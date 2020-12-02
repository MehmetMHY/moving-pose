from collections import defaultdict
import pickle
import os

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

    def fit(self, X, y, cache_path=None, X_is_normalized=True, verbose=False):
        """
        Fit this estimator with provided training data

        Parameters
        ----------
        :param X: training features
          Format: [[[[x, y, z, x', y', z', x'', y'', z'', t] ... (all descriptors)] ... (all poses)] .. (all actions)]
        :param y: training labels
          Format: [str(action) ... (all actions)]
        :param cache_path: Path to cached training results
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

        self._frame_poses_dict.clear()

        if cache_path is None or not os.path.exists(cache_path):
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
                    for descriptor in pose:
                        pose_descriptors[0].extend(descriptor[0:3])
                        pose_descriptors[1].extend(descriptor[3:6])
                        pose_descriptors[2].extend(descriptor[6:9])
                    for j in range(3):
                        derivatives[j].append(pose_descriptors[j])
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

            for i in range(len(labels)):
                if i % 1000 == 0 and verbose:
                    print(f"V-Score progress: {round(i/len(labels), 3)*100}%")
                cur_pose_derivatives = [derivatives[j][i] for j in range(3)]
                cur_label = labels[i]
                cur_v = []
                for traditional_knn, cur_pose_derivative in zip(traditional_knns, cur_pose_derivatives):
                    neighbors = traditional_knn.kneighbors(
                        [cur_pose_derivative],
                        return_distance=False
                    )

                    same_class_sum = 0
                    for neighbor in neighbors[0]:
                        if cur_label == labels[neighbor]:
                            same_class_sum += 1

                    cur_v.append(same_class_sum / len(neighbors[0]))
                vs.append(cur_v)
            if verbose:
                print("Complete")

            if cache_path is not None:
                with open(cache_path, 'wb') as fp:
                    pickle.dump(
                        (derivatives, labels, frames, traditional_knns, vs),
                        fp,
                        protocol=pickle.HIGHEST_PROTOCOL
                    )
        else:
            with open(cache_path, 'rb') as fp:
                derivatives, labels, frames, traditional_knns, vs = pickle.load(fp)

        if verbose:
            print("Creating self._frame_poses_dict...", end=" ")
        # setup dictionary for temporal knn
        # Format: _frame_descriptors_dict[frame] = [[pose, label, v] ... (all poses)]
        #                                   pose = [x, y, z, x', y', z', x'', y'', z'', ... (all descriptors)]
        for i in range(len(frames)):
            cur_frame = frames[i]
            cur_derivatives = [derivatives[j][i] for j in range(3)]
            cur_label = labels[i]
            cur_v = vs[i]

            cur_pose = []
            for k in range(0, 60, 3):
                for j in range(3):
                    cur_pose.extend(cur_derivatives[j][k:k+3])

            v_total = float(cur_v[0]) + self.alpha * cur_v[1] + self.beta * cur_v[2]
            self._frame_poses_dict[cur_frame].append((cur_pose, cur_label, v_total))
        if verbose:
            print("Complete")
            print("---")
            print("Training complete!")

        self.is_fit = True
        return self

    def k_poses(self, X, X_is_normalized=True, return_v=True, verbose=False):
        """
        Get nearest poses

        Parameters
        ----------
        :param X: pose
            Format: [[[x, y, z, x', y', z', x'', y'', z'', t] ... (all descriptors)]
        :param X_is_normalized: boolean denoting whether or not X is normalized
        :param return_v: boolean denoting whether or not pose V score should be returned

        Returns
        -------
        :return: tuple of nearby actions and their variances
            Format: ([action, ... (all poses)], [v_score, ... (all poses)])
        """

        if not self.is_fit:
            raise NotFittedError("The estimator has not been fit")

        if not X_is_normalized:
            raise NotImplemented("Descriptors must be normalized")

        min_range = max(0, X[0, -1] - self.kappa)
        max_range = min(max(self._frame_poses_dict.keys()), X[0, -1] + self.kappa)
        train_range = range(int(min_range), int(max_range))

        # all pose derivatives
        #   Format: [x, y, z, x', y', z', x'', y'', z'', ... (all  descriptors))]
        cur_pose = []
        for descriptor in X:
            cur_pose.extend(descriptor[0:9])

        # all relevant (temporal range) pose derivatives in the following format:
        # [[x, y, z, x', y', z', x'', y'', z'' ... (all descriptors)], ... (all poses)]
        relevant_poses = []

        # all relevant (temporal range) pose v_scores and labels in the following format:
        # [[v_score, label], ... (all poses)]
        relevant_labels_v = []

        for i in train_range:
            relevant_poses.extend(frame_info[0] for frame_info in self._frame_poses_dict[i])
            relevant_labels_v.extend(frame_info[1:] for frame_info in self._frame_poses_dict[i])

        if len(relevant_poses) == 0:
            if verbose:
                print("WARNING :: Relevant poses is empty. Exiting...")
            return []

        traditional_knn = KNeighborsClassifier(
            n_neighbors=min(self.n_neighbors, len(relevant_poses))
        ).fit(relevant_poses, relevant_labels_v)
        neighbors = traditional_knn.kneighbors([cur_pose])[1][0]

        return [relevant_labels_v[label_v] for label_v in neighbors] if return_v \
            else [relevant_labels_v[label_v][0] for label_v in neighbors]

    def get_params(self, deep=True):
        return {
            'alpha': self.alpha, 'beta': self.beta,
            'kappa': self.kappa, 'n_neighbors': self.n_neighbors,
            'n_training_neighbors': self.n_training_neighbors
        }

    def __str__(self):
        return f'alpha={self.alpha}_beta={self.beta}_kappa={self.kappa}' \
               f'_n_neighbors={self.n_neighbors}_n_training_neighbors={self.n_training_neighbors}'
