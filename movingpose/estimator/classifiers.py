import pickle
from collections import defaultdict
import numpy as np

from sklearn.base import BaseEstimator
from sklearn.exceptions import NotFittedError

from movingpose.logic.metrics import max_class_score


def load_pickle(path):
    """
    Load classifier from pickle file
    """
    with open(path, 'rb') as fp:
        data = pickle.load(fp)
    return data


class ActionClassifier(BaseEstimator):

    def __init__(self, nearest_descriptor_estimator, theta=0.3, n=5):
        """
        Initialize action classifier

        Parameters
        ----------
        :param nearest_descriptor_estimator: kNN classifier used for retrieving k nearest action descriptors
                    must contain:
                        fit(X, y): fits the model with relevant descriptors
                        k_descriptors(X): returns an enumerable of actions nearby X and their scores
        :param theta: minimum score to return an action
        :param n: minimum number of frames before making a prediction
        """
        self.action_neighbors_estimator = nearest_descriptor_estimator
        self.theta = theta
        self.n = n

    def fit(self, X, y, actions_are_normalized=True):
        """
        Fit the estimator with relevant actions

        Parameters
        ----------
        :param X: list of actions
           Format: [[[[x, y, z, x', y', z', x'', y'', z'', t] ... (all descriptors)] ... (all poses)] .. (all actions)]
        :param y: list of labels denoting the type of action
           Format: [str(action) ... (all actions)]
        :param actions_are_normalized: boolean denoting whether or not actions are normalized

        Returns
        -------
        :return: self
        """
        # State Changes
        # -------------
        # Fit self.action_neighbors_estimator with X and y

        if not actions_are_normalized:
            raise NotImplemented("Actions must be normalized")

        self.action_neighbors_estimator.fit(X, y, actions_are_normalized)

        return self

    def predict(self, X, descriptors_are_normalized=True):
        """
        Predict action from descriptors

        Parameters
        ----------
        :param X: Action in the form of a temporally ordered list of poses
            Format: [[[x, y, z, x', y', z', x'', y'', z'', t], ... (all descriptors)], ... (all poses)]
        :param descriptors_are_normalized: boolean denoting whether or not descriptors are normalized

        Returns
        -------
        :return: Predicted action
            Format: str(action)
        """

        if X is None:
            raise ValueError("X is required when predicting an action with the Action Classifier")

        if not self.action_neighbors_estimator.is_fit:
            raise NotFittedError("The estimator has not been fit")

        if not descriptors_are_normalized:
            raise NotImplemented("Actions must be normalized")

        class_score = defaultdict(float)
        while (pose := next(X, None)) is not None:
            for nearby_pose, score in self.action_neighbors_estimator.k_poses(pose):
                class_score[nearby_pose] += score
            mcs = max_class_score(class_score, return_total=True)
            if mcs[0][1]/mcs[1] > self.theta:
                return mcs[0][0]
        return max_class_score(class_score)[0]

    def save_pickle(self, path):
        """
        Save `self` to a pickle file located at the provided `path`

        Parameters
        ----------
        :param path: Save location
        """
        if path[-2:] == ".p":
            path = path
        else:
            path = str(path + ".p")

        with open(path, 'wb') as fp:
            pickle.dump(self, fp, protocol=pickle.HIGHEST_PROTOCOL)
