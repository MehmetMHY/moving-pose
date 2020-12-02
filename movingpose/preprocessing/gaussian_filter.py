import numpy as np
# import cv2


# create gaussian filter kernel matrix
def create_kernel(o, n):
     return list(cv2.getGaussianKernel(ksize=n,sigma=o).T[0])


# apply gaussian filter to 1 action of the skeleton data
# notes:
#   - input:  skeleton data for 1 action (x, 20, 5)
#   - output: skeleton data with GF applied (x, 20, 5)
#   - using GF does corrupt each frame's label and joint number,
#     this will we accounted for during training.

KERNEL = [0.05448868, 0.24420134, 0.40261995, 0.24420134, 0.05448868]


def smooth_frames(frame_grouping, kernel):
    """apply guassian filter to set of 5 frames
    :param frame_grouping: group of n frames
    :param kernel: n size kernel to apply to frames
    :return guassian filtered frames
    """
    if len(frame_grouping) != 5:
        raise Exception("Unexpected number of frames in frame grouping")
    for i in range(5):  # 1-5
        kernel_value = kernel[i]
        frame_grouping[i] = frame_grouping[i] * kernel_value
    return sum(frame_grouping)


def gaussian_filter(action_data, kernel=KERNEL):
    """
    :param action_data: data from one action formatted as a np array (frames, 20, 5) [[[frame, joint, x, y, z] for all joints] for all frames]
    :return: np array [[[frame, joint, x, y, z] for all joints] for all frames] with gaussian filter applied
    """
    # frame = data.copy()
    # for frame_i in range(len(frame)):
    #     for joint_j in range(len(frame[frame_i])):
    #         frame[frame_i][joint_j].pop(0)
    #         frame[i][j].pop(0)
    temp = []
    for frame_data_i in range(len(action_data) - 5):
        ans = []
        ans.append(action_data[frame_data_i][:, 2:])
        ans.append(action_data[frame_data_i + 1][:, 2:])
        ans.append(action_data[frame_data_i + 2][:, 2:])
        ans.append(action_data[frame_data_i + 3][:, 2:])
        ans.append(action_data[frame_data_i + 4][:, 2:])
        temp.append(ans)
    temp = np.array(temp)
    
    filtered_data = []
    for frame_data_i in range(len(temp)):
        filtered_data.append(smooth_frames(temp[frame_data_i], kernel))
    filtered_data = np.array(filtered_data)
    # (frames, 20, 3) -> (frames, 20, 5)
    # add joint and frame number back in
    joint_numbers = action_data[0, :, 1]
    joint_numbers = joint_numbers.reshape((1, -1))

    finalized_filtered_values = []
    for frame_data_i in range(len(filtered_data)):
        frame_num = np.full((1, 20), frame_data_i + 1)
        frame_joints = np.insert(filtered_data[frame_data_i], 0, joint_numbers, axis=1)
        frame_frames = np.insert(frame_joints, 0, frame_num, axis=1)
        finalized_filtered_values.append(frame_frames)

    for frame_data_i in range(len(action_data) - 5, len(action_data)):
        finalized_filtered_values.append(action_data[frame_data_i])

    return np.array(finalized_filtered_values)