from collections import defaultdict
import numpy as np

from sklearn.base import BaseEstimator
from sklearn.exceptions import NotFittedError

from logic.metrics import max_class_score

            # for each descriptor calculate the probability it belongs to its own class

class ActionClassifier(BaseEstimator):

    def __init__(self, descriptor_neighbors_estimator, theta=0.3, n=5):
        """
        Initialize action classifier

        Parameters
        ----------
        :param descriptor_neighbors_estimator: kNN classifier used for retrieving k nearest action descriptors
                    must contain:
                        fit(X, y): fits the model with relevant descriptors
                        k_descriptors(X): returns an enumerable of actions nearby X and their scores
        :param theta: minimum score to return an action
        :param n: minimum number of frames before making a prediction
        """
        self.action_neighbors_estimator = descriptor_neighbors_estimator
        self.theta = theta
        self.n = n

    def fit(self, actions, action_labels, actions_are_normalized=True, save_train_data=False):
        """
        Fit the estimator with relevant actions

        Parameters
        ----------
        :param actions: Ordered lists of descriptors making up actions
        :param action_labels: array of labels denoting the type of action
        :param actions_are_normalized: boolean denoting whether or not actions are normalized

        Returns
        -------
        :return: self
        """

        if not actions_are_normalized:
            raise NotImplemented("Actions must be normalized before they can be used to fit the Action Classifier")

        descriptors = []
        descriptor_labels = []
        for action, label in zip(actions, action_labels):
            descriptor_labels.extend([label] * len(action))
            descriptors.extend(action)

        descriptors = np.array(descriptors)
        descriptor_labels = np.array(descriptor_labels)

        self.action_neighbors_estimator.fit(descriptors, descriptor_labels, save_train_data)
        return self

    def predict(self, action=None, descriptors_are_normalized=True, key=None):
        """
        Predict action from descriptors

        Parameters
        ----------
        :param action: ordered list of descriptors (temporal!) describing an action (required when key is None)
        :param descriptors_are_normalized: boolean denoting whether or not descriptors are normalized
        :param key: function that retrieves next descriptor when called (required when descriptors is None)
                        key must return temporal location or 'None' to terminate

        Note: When action and key are provided, action is used

        Returns
        -------
        :return: predicted action as iterable
        """

        if action is None and key is None:
            raise ValueError("Value for action or key is required when predicting an action with the Action Classifier")

        if not self.action_neighbors_estimator.is_fit:
            raise NotFittedError("The Action Classifier is not fit")

        if not descriptors_are_normalized:
            raise NotImplemented("Actions must be normalized before predictions can be made with the Action Classifier")

        if action is not None:
            action = iter(action)

        class_score = defaultdict(float)
        while (descriptor := next(action, None) if action is not None else key()) is not None:
            for train_action, score in self.action_neighbors_estimator.k_descriptors(descriptor):
                class_score[train_action] += score
            mcs = max_class_score(class_score, return_total=True)
            if mcs[0][1]/mcs[1] > self.theta:
                yield mcs[0][0]
        yield max_class_score(class_score)[0]
