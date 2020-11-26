from collections import defaultdict

from sklearn.base import BaseEstimator
from sklearn.exceptions import NotFittedError
from sklearn.neighbors import KNeighborsClassifier
from movingpose.logic.metrics import manhattan_temporal_delta_quant


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

    def fit(self, X, y, X_is_normalized=True):
        """
        Fit this estimator with provided training data

        Parameters
        ----------
        :param X: training features (descriptors: [[x, y, z, x', y', z', x'', y'', z'', t] ... (all descriptors)])
        :param y: training labels (action)
        :param X_is_normalized: boolean denoting whether or not training features are normalized

        Returns
        -------
        :return: self
        """

        if not X_is_normalized:
            raise NotImplemented("X must be normalized")

        # all descriptors' (x,y,z), (x', y', z'), and (x'', y'', z'')
        derivatives = [X[:, 0:3], X[:, 3:6], X[:, 6:9]]

        # list of frame numbers
        frames = X[:, -1]

        # KNN estimator fit with `derivatives`
        #       Format: [(knn pos), (knn pos)', (knn pos)'']
        traditional_knns = []

        # v scores for every derivative
        #       Format: [[v, v', v''] ... (all descriptors) ]
        vs = []

        # Train all traditional knns using each `derivative` (X) and labels (y)
        for derivative in derivatives:
            traditional_knns.append(KNeighborsClassifier(n_neighbors=self.n_training_neighbors).fit(derivative, y))

        for descriptor, label in zip(X, y):
            descriptor_v = []
            for traditional_knn, derivative in zip(traditional_knns, [descriptor[0:3], descriptor[3:6], descriptor[6:9]]):
                neighbors = traditional_knn.kneighbors(derivative.reshape((1, -1)), return_distance=False)

                same_class_sum = 0
                # loop through all neighbors
                for i in neighbors[0]:
                    # if the neighbor shares a label with the current descriptor then increase the count of same class
                    if label == y[i]:
                        same_class_sum += 1
                    
                descriptor_v.append(same_class_sum / len(neighbors[0]))
            vs.append(descriptor_v)

        # setup dictionary for temporal knn, format _frame_descriptors_dict[frame] = [descriptor, v, label]
        for frame, descriptor, v, label in zip(frames, X, vs, y):
                self._frame_descriptors_dict[frame].append((descriptor, v, label))

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

