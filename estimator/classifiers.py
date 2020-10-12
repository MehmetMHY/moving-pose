from sklearn.base import BaseEstimator


class ActionClassifier(BaseEstimator):

    def __init__(self, descriptor_neighbors_estimator, n=5):
        """
        Initialize action classifier

        Parameters
        ----------
        :param descriptor_neighbors_estimator: kNN classifier used for retrieving k nearest action descriptors
                    must contain:
                        fit(X): fits the model with relevant descriptors
                        k_descriptors(X): returns an enumerable of descriptors and their scores
        :param n: minimum number of frames before making a prediction
        """
        self.action_neighbors_estimator = descriptor_neighbors_estimator
        self.n = n

    def fit(self, actions, action_labels, actions_are_normalized=True):
        """
        Fit the estimator with relevant actions

        Parameters
        ----------
        :param actions: Ordered list of descriptors making up an action
        :param action_labels: array of labels denoting the type of action
        :param actions_are_normalized: boolean denoting whether or not actions are normalized

        Returns
        -------
        :return: self
        """
        return self

    def predict(self, descriptors, descriptors_are_normalized=True):
        """
        Predict action from descriptors

        Parameters
        ----------
        :param descriptors: ordered list of descriptors describing a pose
        :param descriptors_are_normalized: boolean denoting whether or not descriptors are normalized

        Returns
        -------
        :return: Predicted action
        """
        pass