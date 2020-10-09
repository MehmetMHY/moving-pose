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
    """:param A frames x 3 matrix containing normalized positions
       :return A frames x 3 matrix containing the first derivative of the positions with respect to time
                output size will contain fewer frames due to the buffer around the current frame"""

def second_derivative(norm_frames):
    """:param A frames x 3 matrix containing first derivatives
       :return A frames x 3 matrix containing 2nd derivatives of position with respect to time"""