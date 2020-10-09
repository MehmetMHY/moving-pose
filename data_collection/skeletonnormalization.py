import numpy as np
from numpy import linalg
from logic.iterators import Skeleton


# set the hip joint to (0, 0) and shift all other joints accordingly
def zero_to_hip(joints_array):
    hip_array = np.full((20, 4), [0, *joints_array[0][1:]])
    return joints_array - hip_array


def delta_vector(start_pt, end_pt):
    return end_pt - start_pt


def normalize_segment(start, start_norm, end, r):
    d_i = delta_vector(start, end)
    d_norm_i = r * d_i / linalg.norm(d_i)
    return start_norm + d_norm_i


def normalize_skeleton(joint_data, R):
    joints = zero_to_hip(joint_data)
    skele = Skeleton(joints)
    joints = skele.get_joints()
    norm_joints = list([None] * 20)
    norm_joints[0] = skele.get_joints()[1]
    for joint_inds, r in zip(skele.get_segments(), R):
        start_ind, end_ind = joint_inds
        start, end = joints[start_ind], joints[end_ind]
        norm_end_joint = normalize_segment(start, norm_joints[start_ind-1], end, r)
        norm_joints[end_ind-1] = norm_end_joint
    return np.array(norm_joints).reshape((20, 3))


# from find_R import *
#
# train = gd.loadData('train.p')
#
# # a08_s01_e01_skeleton_proj.txt         hands raised over head
# # a10_s06_e02_skeleton_proj.txt         wave
# action_data = train["a08_s01_e01_skeleton_proj.txt"]
# print(np.array(action_data).shape)
# print(np.array(action_data)[0,:,:].shape) # frame 1
#
# def get_frame(frame, data):
#     return np.array(data)[frame - 1,:,1:]
#
# test_frame = get_frame(1, action_data)
# R = avg_dis_r(train)
#
#
#
# print(normalize_skeleton(test_frame, R))