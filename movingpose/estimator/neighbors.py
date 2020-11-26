from collections import defaultdict

from sklearn.base import BaseEstimator
from sklearn.exceptions import NotFittedError
from sklearn.neighbors import KNeighborsClassifier
from movingpose.logic.metrics import manhattan_temporal_delta_quant

import movingpose.preprocessing.kinect_skeleton_data as gd
from datetime import datetime


class NearestDescriptors(BaseEstimator):

    def __init__(self, n_neighbors=5, n_training_neighbors=10, alpha=0.6, beta=0.2, kappa=3,
                 temporal_delta_quant=manhattan_temporal_delta_quant):
        """
        Initialize NearestDescriptors Estimator

        Parameters
        ----------
        :param n_neighbors: number of nearest descriptors to return
        :param n_training_neighbors: number of nearest neighbors to include when generating descriptor scores
        TODO(Add alpha and beta weights)
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

    def fit(self, X, y, X_is_normalized=True, save_train_data=False):
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
        # lines 51 to 65 find v scores for each descriptor
        vs = []
        descriptors = X[:, :-1]
        ts = X[:, -1]
        traditional_knn = KNeighborsClassifier(n_neighbors=self.n_training_neighbors)\
            .fit(descriptors, y)  #[descriptor[:-1] for descriptor in X], y)

        for descriptor, label in zip(descriptors, y):
            # for each descriptor calculate the probability it belongs to its own class
            neighbors = traditional_knn.kneighbors(descriptor.reshape((1, -1)), return_distance=False)
            same_class_sum = 0
            # loop through all neighbors
            # TODO vs are larger than one I don't think this should ever happen
            for i in neighbors[0]:
                # if the neighbor shares a label with the current descriptor then increase the count of same class
                if label == y[i]:
                    same_class_sum += 1
            # variance is equal to the number of neighbors that share a label over the total number of neighbors
            vs.append(float(same_class_sum)/len(neighbors[0]))

        # setup dictionary for temporal knn, frame (t) : descriptor (without t)
        for descriptor, label, v, t in zip(descriptors, y, vs, ts):
                self._frame_descriptors_dict[t].append((descriptor, label, v))

        self.is_fit = True

        if save_train_data:
            time_stamp = datetime.now().strftime('%m-%d-%H-%M')
            gd._save_data(f'train_data-{time_stamp}', self._frame_descriptors_dict)
        return self

    def load_train_data(self, filename):
        self._frame_descriptors_dict = gd.load_pickle(filename)
        self.is_fit = True

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

        position = X[:-1]  # slice t out of descriptor
        train_range = range(max(0, X[-1] - self.kappa), min(max(self._frame_descriptors_dict.items()), X[-1] + self.kappa))

        descriptors = []
        labels_v = []
        for i in train_range:
            descriptors.extend(descriptor[0] for descriptor in self._frame_descriptors_dict[i])
            labels_v.extend([tuple([label, v]) for _, label, v in self._frame_descriptors_dict[i]])

        traditional_knn = KNeighborsClassifier(n_neighbors=self.n_neighbors)\
            .fit(descriptors, labels_v)

        return traditional_knn.kneighbors(position) if return_v \
            else [value_only[0] for value_only in traditional_knn.kneighbors(position)]
