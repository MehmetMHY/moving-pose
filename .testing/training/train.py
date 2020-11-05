from estimator.classifiers import ActionClassifier
from estimator.neighbors import NearestDescriptors
from preprocessing.generate_mps import generate_mps


data = generate_mps('../../pickle/train.p')
actions = [action for action, _ in data.values()]
labels = [label for _, label in data.values()]

knn_estimator = NearestDescriptors()
print('Initialized knn estimator')
classifier = ActionClassifier(knn_estimator)
print('Initialized action classifier')
print('Fitting classifier')
classifier.fit(actions, labels)
print('Fitting finished')

