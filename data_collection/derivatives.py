"""At a given moment in time, a certain posetogether with specific movements of the 3D body joints
second order derivativesδP(t0) and δ^2P(t0). The derivatives are estimated numerically by using a
 temporal window of 5 frames centered at the current one processed:
 δP(t0)≈P(t1)−P(t−1) and δ^2P(t0)≈P(t2)+P(t−2)−2P(t0)"""

# TODO gaussian smoothing must be done first
# TODO derivatives are calculated using the normalized model

# δP(t0)≈P(t1)−P(t−1)
# the velocity at  P(t0) is equal to the difference between the position of P at t1 and t_-1
import numpy as np


def first_derivative(norm_frames):
    """:param norm_frames A frames x joints x 3 numpy array containing normalized positions [x_i, y_i, z_i], minimum of
              3 frames
       :return A frames x 3 numpy array containing the first derivative of the positions with respect to time
                output size will contain fewer frames due to the buffer around the current frame"""

    derivatives = np.empty((0, norm_frames.shape[1], 3))
    # for every pose at time t in sequence of poses
    for t in range(len(norm_frames)):
        # if derivative can be calculated at frame t calculate it
        if t in range(1, len(norm_frames) - 1):
            derivative_t = norm_frames[t + 1] - norm_frames[t - 1]
            derivatives = np.append(derivatives, np.array([derivative_t]), axis=0)
        # if derivative cannot be calculated at time t create NaN values for every position of joints
        else:
            derivative_t = np.array([[[np.NaN, np.NaN, np.NaN] for joints in norm_frames[t]]])
            derivatives = np.append(derivatives, derivative_t, axis=0)
    return derivatives


def second_derivative(norm_frames):
    """ :param norm_frames A frames x joints x 3 numpy array containing positions for all joints at frame t, minimum of 5 frames
        :return A frames x joints x 3 numpy array containing 2nd derivatives of position with respect to time"""
    second_derivatives = np.empty((0, norm_frames.shape[1], 3), float)
    for t in range(len(norm_frames)):
        if t in range(2, len(norm_frames) - 2):
            second_derivative_t = norm_frames[t + 2] + norm_frames[t - 2] - 2 * norm_frames[t]
            second_derivatives = np.append(second_derivatives, np.array([second_derivative_t]), axis=0)
        else:
            second_derivative_t = np.array([[[np.NaN, np.NaN, np.NaN] for joints in norm_frames[t]]])
            second_derivatives = np.append(second_derivatives, second_derivative_t, axis=0)

    return second_derivatives
