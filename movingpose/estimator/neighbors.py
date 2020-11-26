from collections import defaultdict

from sklearn.base import BaseEstimator
from sklearn.exceptions import NotFittedError
from sklearn.neighbors import KNeighborsClassifier


class NearestPoses(BaseEstimator):

    def __init__(self, n_neighbors=5, n_training_neighbors=10, alpha=0.6, beta=0.2, kappa=3):
        """
        Initialize NearestPoses Estimator

        Parameters
        ----------
        :param n_neighbors: number of nearest poses to return
        :param n_training_neighbors: number of nearest neighbors to return
        :param alpha: derivative (speed) of pose weight
        :param beta: double derivative (acceleration) of pose weight
        :param kappa: max temporal delta to filter training data with when calling k_poses
        """
        self.n_neighbors = n_neighbors
        self.n_training_neighbors = n_training_neighbors
        self.alpha = alpha
        self.beta = beta
        self.kappa = kappa

        self.is_fit = False
        self._frame_poses_dict = defaultdict(list)

    def fit(self, X, y, X_is_normalized=True):
        """
        Fit this estimator with provided training data

        Parameters
        ----------
        :param X: training features
          Format: [[[[x, y, z, x', y', z', x'', y'', z'', t] ... (all descriptors)] ... (all poses)] .. (all actions)]
        :param y: training labels
          Format: [str(action) ... (all actions)]
        :param X_is_normalized: boolean denoting whether or not training features are normalized

        State Changes
        -------------
        self._frame_descriptors_dict : Dictionary used by temporal knn
            Format: _frame_poses_dict[frame] = [(pose, v, label) ... (all poses at `frame`)]
                                        pose = [x, y, z, x', y', z', x'', y'', z'', ... (all descriptors)]
                                           v = [v_score, v'_score, v''_score]
                                       label = str(action)

        Returns
        -------
        :return: self
        """

        if not X_is_normalized:
            raise NotImplemented("X must be normalized")

        # all pose derivatives in the following format:
        # [
        #   [(x,y,z, ... (all descriptors)), ... (all poses)],
        #   [(x', y', z', ... (all descriptors)), ... (all poses)],
        #   [(x'', y'', z'', ... (all  descriptors)), ... (all poses)]
        # ]
        derivatives = [[], [], []]

        # all pose labels in the following format:
        # [
        #   str(action1), str(action1), ... (all poses in action1),
        #   str(action2), str(action2), ... (all poses in action2),
        # ...  (all actions)]
        labels = []

        # each pose's frame number
        frames = []

        for i, action in enumerate(X):
            for pose in action:
                pose_descriptors = [[], [], []]
                for descriptor in pose[0]:
                    pose_descriptors[0].extend(descriptor[0:3])
                    pose_descriptors[1].extend(descriptor[3:6])
                    pose_descriptors[2].extend(descriptor[6:9])
                derivatives[0].append(pose_descriptors[0])
                derivatives[1].append(pose_descriptors[1])
                derivatives[2].append(pose_descriptors[2])
                labels.append(y[i])
                frames.append(pose[0][-1])

        # KNN estimator fit with `derivatives`
        #       Format: [knn, knn', knn'']
        traditional_knns = [
            KNeighborsClassifier(n_neighbors=self.n_training_neighbors).fit(derivatives[i], labels) for i in range(3)
        ]

        # v scores for every derivative
        #       Format: [[v, v', v''] ... (all poses) ]
        vs = []

        for i in range(len(frames)):
            cur_pose_derivatives = [derivatives[0][i], derivatives[1][i], derivatives[2][i]]
            cur_label = labels[i]
            cur_v = []
            for traditional_knn, cur_pose_derivative in zip(traditional_knns, cur_pose_derivatives):
                neighbors = traditional_knn.kneighbors(cur_pose_derivative.reshape((1, -1)), return_distance=False)

                same_class_sum = 0
                for neighbor in neighbors[0]:
                    if cur_label == neighbor:
                        same_class_sum += 1

                cur_v.append(same_class_sum / len(neighbors[0]))
            vs.append(cur_v)

        # setup dictionary for temporal knn, format _frame_descriptors_dict[frame] = [descriptor, v, label]
        for i in range(len(frames)):
            cur_frame = frames[i]
            cur_pose_derivatives = [derivatives[0][i], derivatives[1][i], derivatives[2][i]]
            cur_label = labels[i]
            cur_v = vs[i]

            self._frame_poses_dict[cur_frame].append((cur_pose_derivatives, cur_v, cur_label))

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
            return [].extend([a for a in self._frame_poses_dict.values()])

        if not X_is_normalized:
            raise NotImplemented("Descriptors must be normalized before calling k_descriptors")

        position = X[:-1]  # slice t out of descriptor
        train_range = range(max(0, X[-1] - self.kappa), min(max(self._frame_poses_dict.items()), X[-1] + self.kappa))

        descriptors = []
        labels_v = []
        for i in train_range:
            descriptors.extend(descriptor[0] for descriptor in self._frame_poses_dict[i])
            labels_v.extend([tuple([label, v]) for _, label, v in self._frame_poses_dict[i]])

        traditional_knn = KNeighborsClassifier(n_neighbors=self.n_neighbors)\
            .fit(descriptors, labels_v)

        return traditional_knn.kneighbors(position) if return_v \
            else [value_only[0] for value_only in traditional_knn.kneighbors(position)]

