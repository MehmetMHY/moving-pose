from estimator.neighbors import NearestDescriptors
from estimator.classifiers import ActionClassifier
from preprocessing.generate_mps import generate_mps
import time


def get_fit_classifier():
    knd = NearestDescriptors()
    classifier = ActionClassifier(knd)

    try:
        knd.load_train_data('train_output.p')
        print('Successfully loaded training data')
    except FileNotFoundError:
        usr_in = input('Could  not load training data would you like to fit model (y/n)')
        if usr_in != 'y':
            return
        data = generate_mps('../../pickle/train.p')
        actions = [action for action, _ in data.values()]
        labels = [label for _, label in data.values()]
        start = time.time()
        classifier.fit(actions, labels)
        end = time.time()
        print('Fitting finished')
        print(f'Time taken: {end - start}')
    return classifier


classifier = get_fit_classifier()



