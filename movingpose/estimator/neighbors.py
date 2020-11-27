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

        Returns
        -------
        :return: self
        """
        # State Changes
        # -------------
        # self._frame_descriptors_dict : Dictionary used by temporal knn
        #     Format: _frame_poses_dict[frame] = [(pose, label, v) ... (all poses at `frame`)]
        #                                 pose = [x, y, z, x', y', z', x'', y'', z'', ... (all descriptors)]

        if not X_is_normalized:
            raise NotImplemented("X must be normalized")

        # all pose derivatives in the following format:
        # [
        #   [[x, y, z, ... (all descriptors)], ... (all poses)],
        #   [[x', y', z', ... (all descriptors)], ... (all poses)],
        #   [[x'', y'', z'', ... (all  descriptors)], ... (all poses)]
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
                for j in range(3):
                    derivatives[i].append(pose_descriptors[i])
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

        # setup dictionary for temporal knn
        # Format: _frame_descriptors_dict[frame] = [[pose, label, v] ... (all poses)]
        #                                   pose = [x, y, z, x', y', z', x'', y'', z'', ... (all descriptors)]
        for i in range(len(frames)):
            cur_frame = frames[i]
            cur_pose = []
            cur_pose.extend([derivatives[j][i] for j in range(3)])
            cur_label = labels[i]
            cur_v = vs[i]

            v_total = float(cur_v[0]) + self.alpha * cur_v[1] + self.beta * cur_v[2]
            self._frame_poses_dict[cur_frame].append((cur_pose, cur_label, v_total))

        self.is_fit = True
        return self

    def k_poses(self, X=None, X_is_normalized=True, return_v=True):
        """
        Get nearest poses

        Parameters
        ----------
        :param X: pose (default returns all poses)
            Format: [[x, y, z, x', y', z', x'', y'', z'', t] ... (all descriptors)]
        :param X_is_normalized: boolean denoting whether or not X is normalized
        :param return_v: boolean denoting whether or not pose V score should be returned

        Returns
        -------
        :return: enumerable of nearby actions and their variances
            Format: ([action, ... (all poses)], [v_score, ... (all poses)])
        """

        if not self.is_fit:
            raise NotFittedError("The estimator has not been fit")

        if X is None:
            all_actions = []
            all_actions.extend([frame_info[2] for frame_info in self._frame_poses_dict])
            all_vs = []
            all_vs.extend([frame_info[1] for frame_info in self._frame_poses_dict])

            return (all_actions, all_vs) if return_v else all_actions

        if not X_is_normalized:
            raise NotImplemented("Descriptors must be normalized")

        min_range = max(0, X[-1] - self.kappa)
        max_range = min(max(self._frame_poses_dict.keys()), X[-1] + self.kappa)
        train_range = range(min_range, max_range)

        # all pose derivatives
        #   Format: [x, y, z, x', y', z', x'', y'', z'', ... (all  descriptors))]
        cur_pose = []
        cur_pose.extend(X[:, 0:9])

        # all relevant (temporal range) pose derivatives in the following format:
        # [[x, y, z, x', y', z', x'', y'', z'' ... (all descriptors)], ... (all poses)]
        relevant_poses = []

        # all relevant (temporal range) pose v_scores and labels in the following format:
        # [[v_score, label], ... (all poses)]
        relevant_labels_v = []

        for i in train_range:
            relevant_poses.append(*frame_info[0] for frame_info in self._frame_poses_dict[i])
            labels = [frame_info[1] for frame_info in self._frame_poses_dict[i]]
            vs = [frame_info[2] for frame_info in self._frame_poses_dict[i]]
            for label, v in zip(labels, vs):
                relevant_labels_v.append([label, v])

        traditional_knn = KNeighborsClassifier(n_neighbors=self.n_neighbors).fit(relevant_poses, relevant_labels_v)
        neighbors = traditional_knn.kneighbors(cur_pose)[0]

        return neighbors if return_v else neighbors[0]
