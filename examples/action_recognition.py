import multiprocessing
import os
import pickle
import sys
from sklearn.model_selection import train_test_split
import uuid
import time

sys.path.append("..")

from movingpose.estimator import neighbors
from movingpose.estimator import classifiers

from movingpose.preprocessing import moving_pose
from movingpose.preprocessing import kinect_skeleton_data

cur_uuid = str(input("cur_uuid (press `enter` to create a new model):"))
dir_path = f"../pickle/{cur_uuid}"

if not (cur_uuid != "" and os.path.isdir(dir_path)):
    print("Creating data...")

    # Load pickled multiview action data
    raw_data_dict = kinect_skeleton_data.load_pickle("../pickle/multiview.p")

    X, labels = moving_pose.format_skeleton_data_dict(raw_data_dict)

    # Verify shape is correct
    for action in X:
        for frame_num, pose in enumerate(action):
            assert pose.shape == (20, 10), f"{pose.shape} =/= (20, 10)"
            for i, descriptor in enumerate(pose):
                if i == 0:
                    assert list(descriptor)[:-1] == [0, 0, 0, 0, 0, 0, 0, 0, 0]
                assert descriptor[-1] == frame_num, f"{descriptor[-1]} =/= {frame_num}"

    X_train, X_test, y_train, y_test = train_test_split(X, labels, random_state=42)

    cur_uuid = str(uuid.uuid4())[0:8]
    dir_path = f"../pickle/{cur_uuid}"

    training_data = {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test
    }

    os.mkdir(dir_path)
    with open(f'../pickle/{cur_uuid}/train_test_splits.p', 'wb') as file:
        pickle.dump(training_data, file)

print("Loading data...")

with open(dir_path + "/train_test_splits.p", 'rb') as fp:
    training_data = pickle.load(fp)

X_train, X_test = training_data["X_train"], training_data["X_test"]
y_train, y_test = training_data["y_train"], training_data["y_test"]


def pickle_action_classifiers(n_training_neighbors, cache_path):
    nearest_pose_estimator = neighbors.NearestPoses(
        n_neighbors=20,
        n_training_neighbors=n_training_neighbors,
        alpha=0.75,
        beta=0.6,
        kappa=80
    )
    action_classifier = classifiers.ActionClassifier(
        nearest_pose_estimator=nearest_pose_estimator,
        theta=0.5,
        n=80
    )
    action_classifier.fit(
        X_train,
        y_train,
        cache_path=cache_path,
        verbose=True
    )


cache_workers = []
for n_training_neighbors in [2000, 5000, 20000]:
    cache_path = f"../pickle/{cur_uuid}/action_classifier_cache-{str(n_training_neighbors)}.p"
    if not os.path.exists(cache_path):
        worker = multiprocessing.Process(
            target=
            pickle_action_classifiers,
            args=(
                n_training_neighbors,
                cache_path
            )
        )
        cache_workers.append(worker)

for cache_worker in cache_workers:
    cache_worker.start()

for cache_worker in cache_workers:
    cache_worker.join()


def score(n_neighbors, n_training_neighbors, alpha, beta, kappa, theta, n):
    nearest_pose_estimator = neighbors.NearestPoses(
        n_neighbors=n_neighbors,
        n_training_neighbors=n_training_neighbors,
        alpha=alpha,
        beta=beta,
        kappa=kappa
    )
    action_classifier = classifiers.ActionClassifier(
        nearest_pose_estimator=nearest_pose_estimator,
        theta=theta,
        n=n
    )
    action_classifier.fit(
        X_train,
        y_train,
        cache_path=f"../pickle/{cur_uuid}/action_classifier_cache-{str(n_training_neighbors)}.p"
    )

    pred_start_time = time.time()
    y_pred = action_classifier.predict_all(X_test, verbose=True)
    total_time = time.time() - pred_start_time
    total_mins = total_time/60

    result = 0
    for pred, actual in zip(y_pred, y_test):
        result += 1 if pred == actual else 0
    print(f"Predicted {result}/{len(y_pred)}")

    prediction_info = {
        "y_pred": y_pred,
        "prediction_speed": total_mins,
        "action_classifier_name": str(action_classifier),
        "action_classifier_params": action_classifier.get_params()
    }

    with open(f'../pickle/{cur_uuid}/prediction-[{action_classifier}].p', 'wb') as file:
        pickle.dump(prediction_info, file)


workers = []
for kappa in [50]:
    for n in [100]:
        for theta in [0.7]:
            for n_neighbors in [10, 50, 100]:
                for n_training_neighbors in [2000, 5000, 20000]:
                    for alpha in [0.75]:
                        for beta in [0.6]:
                            worker = multiprocessing.Process(
                                target=
                                    score,
                                args=(
                                    n_neighbors,
                                    n_training_neighbors,
                                    alpha,
                                    beta,
                                    kappa,
                                    theta,
                                    n
                                )
                            )
                            workers.append(worker)

num_cpu_cores = os.getenv("NUM_CPU_CORES")
if num_cpu_cores is None:
    num_cpu_cores = input("Enter the number of CPU cores this computer has (ex. '12'): ")
num_cpu_cores = max(1, int(num_cpu_cores) - 4)

num_workers_executed = num_cpu_cores
while num_workers_executed - num_cpu_cores < len(workers):
    for i in range(num_cpu_cores, max(num_workers_executed - len(workers), 0), -1):
        workers[num_workers_executed - i].start()
    for i in range(num_cpu_cores, max(num_workers_executed - len(workers), 0), -1):
        workers[num_workers_executed - i].join()
    num_workers_executed += num_cpu_cores
