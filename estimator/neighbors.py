from collections import defaultdict

from sklearn.base import BaseEstimator
from sklearn.exceptions import NotFittedError
from sklearn.neighbors import KNeighborsClassifier
from logic.metrics import manhattan_temporal_delta_quant


class NearestDescriptors(BaseEstimator):

    def __init__(self, n_neighbors=5, n_training_neighbors=10, alpha=0.6, beta=0.2, kappa=3,
                 temporal_delta_quant=manhattan_temporal_delta_quant):
        """
        Initialize NearestDescriptors Estimator

        Parameters
        ----------
        :param n_neighbors: number of nearest descriptors to return
        :param n_training_neighbors: number of nearest neighbors to include when generating descriptor scores
        :param alpha: derivative (speed) of P(t) weight
        :param beta: double derivative (acceleration) of P(t) weight
        :param temporal_delta_quant: function to calculate scalar delta between two temporal points
        :param kappa: max temporal delta to filter training data with when calling k_descriptors
        """
        self.n_neighbors = n_neighbors
        self.n_training_neighbors = n_training_neighbors
        self.alpha = alpha
        self.beta = beta
        self.temporal_delta_quant = temporal_delta_quant
        self.kappa = kappa
        self.is_fit = False

        self._frame_descriptors_dict = defaultdict(list)

    def fit(self, X, y, X_is_normalized=True):
        """
        Fit this estimator with provided training data and hyper parameters

        Parameters
        ----------
        :param X: training features (descriptors)
        :param y: training labels (action)
        :param X_is_normalized: boolean denoting whether or not training data is normalized

        Returns
        -------
        :return: self
        """

        vs = []
        traditional_knn = KNeighborsClassifier(n_neighbors=self.n_training_neighbors)\
            .fit([descriptor[:-1] for descriptor in X], y)
        for descriptor, label in zip(X, y):
            neighbors = traditional_knn.kneighbors(descriptor[:-1])
            same_class_sum = 0
            for neighbor, neighbor_label in neighbors:
                if label == neighbor_label:
                    same_class_sum += 1
            vs.append(float(same_class_sum/len(neighbors)))

        for descriptor, label, v in zip(X, y, vs):
                self._frame_descriptors_dict[descriptor[3]].append((descriptor[:-1], label, v))

        self.is_fit = True
        return self

    def k_descriptors(self, X=None, X_is_normalized=True, return_v=True):
        """
        Get nearest descriptors

        Parameters
        ----------
        :param X: current descriptor (default returns all descriptors)
        :param X_is_normalized: boolean denoting whether or not training data is normalized
        :param return_v: boolean denoting whether or not descriptor V score should be returned

        Returns
        -------
        :return: enumerable of nearby actions and their variances
        """

        if not self.is_fit:
            raise NotFittedError("The Action Classifier is not fit")

        if X is None:
            return [].extend([a for a in self._frame_descriptors_dict.values()])

        if not X_is_normalized:
            raise NotImplemented("Descriptors must be normalized before calling k_descriptors")

        position = X[:-1]
        train_range = range(max(0, X[-1] - self.kappa), min(max(self._frame_descriptors_dict.items()), X[-1] + self.kappa))
        train_vals = tuple([[], []])
        for train_ind in train_range:
            train_vals[0].extend([descriptors[0] for descriptors in self._frame_descriptors_dict[train_ind]])
            train_vals[1].extend([tuple([stuff[1], stuff[2]]) for stuff in self._frame_descriptors_dict[train_ind]])

        traditional_knn = KNeighborsClassifier(n_neighbors=self.n_neighbors)\
            .fit(*train_vals)

        return traditional_knn.kneighbors(position)

