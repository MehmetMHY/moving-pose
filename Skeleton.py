
class Skeleton:
    # initialize with array of joints and position [[joint_1, x_1, y_1, z_1],...,[joint_20, x_20, y_20, z_20]]
    def __init__(self, joints_array):
        self._joints = {int(i[0]): i[1:] for i in joints_array}
        self.__BF_ITERATION = [1, 2, 13, 17, 3, 14, 18, 4, 5, 9, 15, 19, 6, 10, 16, 20, 7, 11, 8, 12]
        print(self.__BF_ITERATION)

    # iterate through with for i in skeleton_instance
    def __iter__(self):
        return iter([self._joints[i] for i in self.__BF_ITERATION])


