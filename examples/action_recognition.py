import sys
sys.path.append("..")
from sklearn.model_selection import train_test_split
import numpy as np

from movingpose.estimator import neighbors
from movingpose.estimator import classifiers

from movingpose.preprocessing import moving_pose
from movingpose.preprocessing import kinect_skeleton_data

## Pickle multiview action data

# kinect_skeleton_data.pickle_dir("../pickle/multiview.p", "../ext/dataset/multiview_action/")

## Load pickled multiview action data

raw_data_dict = kinect_skeleton_data.load_pickle("../pickle/multiview.p")

## Format multiview action data

X, labels = moving_pose.format_skeleton_data_dict(raw_data_dict)

## Perform basic verification that skeleton data is formatted correctly

for action in X:
    for frame_num, pose in enumerate(action):
        assert pose.shape == (20, 10), f"{pose.shape} =/= (20, 10)"
        for i, descriptor in enumerate(pose):
            if i == 0:
                assert list(descriptor)[:-1] == [0, 0, 0, 0, 0, 0, 0, 0, 0]
            assert descriptor[-1] == frame_num, f"{descriptor[-1]} =/= {frame_num}"

## Create train/test split

X_train, X_test, y_train, y_test = train_test_split(X, labels, random_state=42)

## Train Action Classifier with normalized training data

print("# Correctly predicted: (higher is better)")
best_score = sys.maxsize
best_action_classifier = None
for n_neighbors in [20, 25, 30]:
    for n_training_neighbors in [2000, 5000, 10000, 20000, 30000, 40000]:
        for alpha in [0.75]:
            for beta in [0.6]:
                for kappa in [20, 30, 40, 50]:
                    nearest_pose_estimator = neighbors.NearestPoses(
                        n_neighbors=n_neighbors,
                        n_training_neighbors=n_training_neighbors,
                        alpha=alpha,
                        beta=beta,
                        kappa=kappa
                    )
                    for theta in [0.6, 0.7, 0.8, 0.9]:
                        for n in [40, 60, 80, 100, 120, 140, 160]:
                            action_classifier = classifiers.ActionClassifier(
                                nearest_pose_estimator=nearest_pose_estimator,
                                theta=theta,
                                n=n
                            )
                            action_classifier.fit(
                                X_train,
                                y_train,
                                cache_path=f"../pickle/action_classifier_training-{str(n_training_neighbors)}.p"
                            )
                            y_pred = action_classifier.predict_all(X_test)

                            correct = 0
                            for pred, actual in zip(y_pred, y_test):
                                correct += 1 if pred == actual else 0

                            print(f"{correct}/{len(y_pred)}")

                            if correct > best_score:
                                best_score = correct
                                best_action_classifier = action_classifier

## Print best action classifier and its score

print(f"The best action classifier was {best_action_classifier}")
print("\n--------------\n")
print(f"Its score was: {best_score}")

## Save the best action classifier

best_action_classifier.save_pickle("../pickle/best_action_classifier.p")

## Load best action classifier

action_classifier = classifiers.load_pickle("../pickle/best_action_classifier.p")

# DAB

print("dab")