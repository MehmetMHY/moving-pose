from estimator.classifiers import ActionClassifier
from estimator.neighbors import NearestDescriptors
from preprocessing.generate_mps import generate_mps
import preprocessing.get_data as gd
import time

data = generate_mps('../../pickle/train.p')
actions = [action for action, _ in data.values()]
labels = [label for _, label in data.values()]

knn_estimator = NearestDescriptors()
print('Initialized knn estimator')
classifier = ActionClassifier(knn_estimator)
print('Initialized action classifier')
print('Fitting classifier')
start = time.time()
classifier.fit(actions, labels)
end = time.time()
print('Fitting finished')
print(f'Time taken: {end - start}')
gd.save_data('train_output', classifier.action_neighbors_estimator._frame_descriptors_dict)

