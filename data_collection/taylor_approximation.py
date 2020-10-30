"""Using the taylor series described in the paper, the position of some joint at time t should be able to be
   approximated using the taylor series P(t)≈P(t0)+δP(t0)(t−t0)+1/2δ^2P(t0)(t−t0)^2. By implementing this
   taylor series we can check that the first and second derivatives were correctly calculated"""

import numpy as np


def approximate(position, first_deriv, second_deriv, t_0, t):
    """:param position a numpy array with x, y, z values for point/s
       :param first_deriv a numpy array with x, y, z values for the first derivative of point/s at t_0
       :param second_deriv a numpy array with x, y z values for the second derivative of point/s at t_0
       :param t_0 the time (frame) the approximation is calculated from,
       :param t the time at which we are trying to approximate a position
       :return a numpy array containing point/s at time t [[x_0, y_0, z_0], ... [x_n, y_n, z_n]]
       The three input arrays (pos, first_deriv, second_deriv) must have the same shape
       First and second derivatives must be definid at t_0
       """

    if not (position.shape == first_deriv.shape == second_deriv.shape):
        raise Exception("Shape of input arrays do not match")

    if np.isnan(first_deriv).flatten().any():
        raise Exception("First derivative undefined at time t_0")

    if np.isnan(second_deriv).flatten().any():
        raise Exception("Second derivative undefined at time t_0")

    interval = t - t_0
    return position + first_deriv * interval + .5 * second_deriv * (interval ** 2)
