from sklearn.base import BaseEstimator
from sklearn.utils.validation import check_X_y, check_is_fitted
from logic.metrics import manhattan_temporal_delta_quant


class NearestDescriptors(BaseEstimator):

    def __init__(self, n_neighbors=5, alpha=0.6, beta=0.2, theta=0.3, kappa=3,
                 temporal_delta_quant=manhattan_temporal_delta_quant):
        """
        Initialize Action Neighbors Estimator

        Parameters
        ----------
        :param n_neighbors: Nearest neighbors
        :param alpha: derivative (speed) of P(t) weight
        :param beta: double derivative (acceleration) of P(t) weight
        :param theta: minimum score to return a pose
        :param temporal_delta_quant: function to calculate scalar delta between two temporal points
        :param kappa: max temporal delta to filter training data with when calling k_descriptors
        """
        self.n_neighbors = n_neighbors
        self.alpha = alpha
        self.beta = beta
        self.theta = theta
        self.temporal_delta_quant = temporal_delta_quant
        self.kappa = kappa

    def fit(self, X, y, X_is_normalized=True):
        """
        Fit this estimator with provided training data and hyper parameters

        Parameters
        ----------
        :param X: training features (descriptors)
        :param y: training labels (action/pose)
        :param X_is_normalized: boolean denoting whether or not training data is normalized

        Returns
        -------
        :return: self
        """
        X, y = check_X_y(X, y)
        # Create nearest neighbors that can easily be looped through from one temporal location to another
        # Generate V(X) scores for all X
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
        :return: enumerable of descriptors (and possibly variances)
        """
        check_is_fitted(self)

        pass
