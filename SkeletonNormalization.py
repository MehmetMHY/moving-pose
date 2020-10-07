import numpy as np
from numpy import linalg as LA
from Skeleton import Skeleton
import math


# set the hip joint to (0, 0) and shift all other joints accordingly
def zero_to_hip(joints_array):
    hip_array = np.full((20, 4), [0, *joints_array[0][1:]])
    return joints_array - hip_array


def delta_vector(start_pt, end_pt):
    return end_pt - start_pt


def normalize_segment(start, start_norm, end, r):
    d_i = delta_vector(start, end)
    d_norm_i = r * d_i / LA.norm(d_i)
    return start_norm + d_norm_i


def normalize_skeleton(joint_data, R):
    joints = zero_to_hip(joint_data)  # TODO check if hip should always be at (0, 0, 0)
    skele = Skeleton(joints)
    norm_joints = [skele.get_joints()[1]]  # list of normalized joint locations
    for joints, r in zip(skele, R):
        start, end = joints
        norm_joints.append(normalize_segment(start, norm_joints[-1], end, r))
    return np.full((20, 3), norm_joints)



import get_data as gd

train = gd.loadData('train.p')
print()
# a08_s01_e01_skeleton_proj.txt         hands raised over head
# a10_s06_e02_skeleton_proj.txt         wave
action_data = train["a08_s01_e01_skeleton_proj.txt"]
print(np.array(action_data).shape)
print(np.array(action_data)[0,:,:].shape) # frame 1

def get_frame(frame, data):
    return np.array(data)[frame - 1,:,1:]

test_frame = get_frame(1, action_data)
R = [1 for i in range(19)]
print(normalize_skeleton(test_frame, R))