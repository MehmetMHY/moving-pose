import numpy as np


class Skeleton:
    # initialize with array of joints and position [[joint_1, x_1, y_1, z_1],...,[joint_20, x_20, y_20, z_20]]
    def __init__(self, joints_array):
        self._joints = {int(i[0]): i[1:] for i in joints_array}
        # joint segments in breadth first order
        self.__segments = ((1, 13), (1, 2), (1, 17), (13, 14), (2, 3),
                           (17, 18), (14, 15), (3, 5), (3, 4), (3, 9),
                           (18, 19), (15, 16), (5, 6), (9, 10), (19, 20),
                           (6, 7), (10, 11), (7, 8), (11, 12))
    # iterate through with for i in skeleton_instance
    # (start, end)
    def __iter__(self):
        return iter([(self._joints[j[0]], self._joints[j[1]]) for j in self.__segments])

    def get_iter(self):
        return self.__segments

    def get_joints(self):
        return self._joints

    def set_joints(self, joints_dict):
        self._joints = joints_dict

    def get_joints_asArray(self):
        return np.array([self._joints[i] for i in self._joints])
