from sklearn.base import BaseEstimator
from sklearn.neighbors import KNeighborsClassifier
from sklearn.utils.validation import check_X_y
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
        scoring_KNN = KNeighborsClassifier(n_neighbors=self.n_training_neighbors).fit(X, y)
        for descriptor in X:
            for nearby_action in scoring_KNN.predict_proba(descriptor):



        # Create nearest neighbors that can easily be looped through from one temporal location to another
        # Generate V(X) scores for all X
        self.is_fit = True
        return self

    def k_descriptors(self, X=None, X_is_normalized=True, return_variance=True):
        """
        Get nearest descriptors

        Parameters
        ----------
        :param X: current descriptor (default returns all descriptors)
        :param X_is_normalized: boolean denoting whether or not training data is normalized
        :param return_variance: boolean denoting whether or not descriptor variance should be returned

        Returns
        -------
        :return: enumerable of nearby actions and their variances
        """

        pass
