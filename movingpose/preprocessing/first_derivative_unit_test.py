import movingpose.preprocessing.kinect_skeleton_data as gd
from movingpose.preprocessing.derivatives import *


# check that every velocity is an array of 3 numbers except for the first and last frame
def check_shape(actual_output, expected_shape=(20, 3)):
    for t in range(len(actual_output)):
        for joint in range(expected_shape[0]):
            if t == 0 or t == len(actual_output) - 1:
                continue
            elif len(actual_output[t, joint]) != expected_shape[1]:
                print(f'Unexpected derivative at {t},{joint}')
                return False
            # the hip is always at the center of the screen so should never have a non-zero derivative
            elif joint == 0 and np.sum(actual_output[t, joint]) != 0:
                print(f'Expected derivative of hip to be 0 was {np.sum(actual_output[t, joint])}')
                return False
    return True


def check_vals(actual_output, expected_output):
    # first and last values should be np.NaN
    if not np.isnan(actual_output[0]).flatten().all():
        return False
    if not np.isnan(actual_output[-1]).flatten().all():
        return False
    return np.allclose(actual_output[1:-1], expected_output[1:-1], rtol=1e-12)


def run_tests():
    #                                joint_1    joint_2     joint_3
    input_array = np.array(np.array([[[0, 0, 0], [0, 0, 0], [0, 0, 0]],    # frame 1
                                    [[0, 0, 0], [0, 0, 0], [0, 0, 0]],    # frame 2
                                    [[1, 1, 1], [1, 1, 1], [1, 1, 1]]]))  # frame 3
    expected_derivative = np.array(np.array([[[np.NaN, np.NaN, np.NaN], [np.NaN, np.NaN, np.NaN], [np.NaN, np.NaN, np.NaN]],
                                             [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
                                             [[np.NaN, np.NaN, np.NaN], [np.NaN, np.NaN, np.NaN], [np.NaN, np.NaN, np.NaN]]]))
    actual_derivative = first_derivative(input_array)
    assert check_vals(actual_derivative, expected_derivative) is True

    input_array = np.array(np.array([[[0, 0, 0], [0, 0, 0], [0, 0, 0]],    # frame 1
                                    [[0, 0, 0], [0, 0, 0], [0, 0, 0]],    # frame 2
                                    [[2, 2, 2], [0, -1, 0], [2.3, 3.99, -400]]]))  # frame 3
    expected_derivative = np.array(np.array([[[np.NaN, np.NaN, np.NaN], [np.NaN, np.NaN, np.NaN],[np.NaN, np.NaN, np.NaN]],
                                             [[2, 2, 2], [0, -1, 0], [2.3, 3.99, -400]],
                                             [[np.NaN, np.NaN, np.NaN], [np.NaN, np.NaN, np.NaN], [np.NaN, np.NaN, np.NaN]]]))
    actual_derivative = first_derivative(input_array)
    assert check_vals(actual_derivative, expected_derivative) is True

    input_array = np.array(np.array([[[1, 1, 1], [1, 1, 1], [1, 1, 1]],  # frame 1
                                     [[0, 0, 0], [0, 0, 0], [0, 0, 0]],  # frame 2
                                     [[2, 2, 2], [0, -1, 0], [2.3, 3.99, -400]]]))  # frame 3
    expected_derivative = np.array(np.array([[[np.NaN, np.NaN, np.NaN], [np.NaN, np.NaN, np.NaN], [np.NaN, np.NaN, np.NaN]],
                                             [[1., 1., 1.], [-1., -2., -1.], [1.3, 2.99, -401.]],
                                             [[np.NaN, np.NaN, np.NaN], [np.NaN, np.NaN, np.NaN], [np.NaN, np.NaN, np.NaN]]]))
    actual_derivative = first_derivative(input_array)
    assert check_vals(actual_derivative, expected_derivative) is True

    norm_train = gd.load_pickle('../pickle/norm_train.p')
    p_t = norm_train['a08_s01_e01_skeleton_proj.txt']
    p_t = np.array([frame for frame in p_t])[:, :, 2:]
    velocity = first_derivative(p_t)
    assert check_shape(velocity) is True

    print("All tests pass")


if __name__ == "__main__":
    run_tests()

