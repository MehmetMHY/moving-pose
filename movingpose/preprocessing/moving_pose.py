import numpy as np

from movingpose.preprocessing import kinect_skeleton_data
from movingpose.preprocessing import gaussian_filter
from movingpose.logic import iterators

file_to_label_dict = {'a01': 'drink',
                      'a02': 'eat',
                      'a03': 'read',
                      'a04': 'write on paper',
                      'a05': 'use laptop',
                      'a06': 'play game',
                      'a07': 'call cellphone',
                      'a08': 'use vacuum cleaner',
                      'a09': 'cheer up',
                      'a10': 'sit still',
                      'a11': 'walking',
                      'a12': 'sit down',
                      'a13': 'toss paper',
                      'a14': 'lay down on sofa',
                      'a15': 'stand up',
                      'a16': 'play guitar'}

r_vector = [0.10476466, 0.07057415, 0.10766335, 0.40250801, 0.31667159,
            0.40411627, 0.29429485, 0.19838387, 0.20443147, 0.20289835,
            0.29255157, 0.09042491, 0.23899638, 0.23617619, 0.09050006,
            0.2313854,  0.2369734,  0.07989741, 0.08361892]


# set the hip joint to (0, 0) and shift all other joints accordingly
def zero_to_hip(joints_array):
    hip_array = np.full((20, 4), [0, *joints_array[0][1:]])
    return joints_array - hip_array


def delta_vector(start_pt, end_pt):
    return end_pt - start_pt


def normalize_segment(start, start_norm, end, r):
    d_i = delta_vector(start, end)
    if np.linalg.norm(d_i) == 0:
        return start_norm
    d_norm_i = r * d_i / np.linalg.norm(d_i)
    return start_norm + d_norm_i


def normalize_skeleton(joint_data, R):
    """
    :param joint_data: 20, 4 matrix of all 20 joints in kinect skeleton data
    :param R: vector of average lengths of joint segments
    :return: joint data 20, 3 matrix of all 20 joints in kinect skeleton normalized
    """
    joints = zero_to_hip(joint_data)
    skele = iterators.Skeleton(joints)
    joints = skele.get_joints()
    norm_joints = list([None] * 20)
    norm_joints[0] = skele.get_joints()[1]
    for joint_inds, r in zip(skele.get_segments(), R):
        start_ind, end_ind = joint_inds
        start, end = joints[start_ind], joints[end_ind]
        norm_end_joint = normalize_segment(start, norm_joints[start_ind - 1], end, r)
        norm_joints[end_ind-1] = norm_end_joint
    return np.array(norm_joints).reshape((20, 3))


def first_derivative(norm_frames):
    """
    :param norm_frames A frames x joints x 3 numpy array containing normalized positions [x_i, y_i, z_i], minimum of
              3 frames
    :return A frames x 3 numpy array containing the first derivative of the positions with respect to time
            output size will contain fewer frames due to the buffer around the current frame
    """

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
    """
    :param norm_frames A frames x joints x 3 numpy array containing positions for all joints at frame t, minimum of 5 frames
    :return A frames x joints x 3 numpy array containing 2nd derivatives of position with respect to time
    """
    second_derivatives = np.empty((0, norm_frames.shape[1], 3), float)
    for t in range(len(norm_frames)):
        if t in range(2, len(norm_frames) - 2):
            second_derivative_t = norm_frames[t + 2] + norm_frames[t - 2] - 2 * norm_frames[t]
            second_derivatives = np.append(second_derivatives, np.array([second_derivative_t]), axis=0)
        else:
            second_derivative_t = np.array([[[np.NaN, np.NaN, np.NaN] for joints in norm_frames[t]]])
            second_derivatives = np.append(second_derivatives, second_derivative_t, axis=0)
    return second_derivatives


def avg_dis_r(data):
    bodies = []
    for file_name, action_frames in data.items():
        for frame in action_frames:
            body = []
            skele = s.Skeleton(np.array(frame)[:, 1:])
            for start, end in skele:
                segment = distance(start, end)
                body.append(segment)
            bodies.append(body)
    R = np.mean(np.array(bodies), axis=0)
    return R / numpy.linalg.norm(R)


# generates R using the training data
def generate_r():
    """
    :return:  find the average distance between every pair of joints in a skeleton used for normalization
    """
    train = kinect_skeleton_data.load_pickle("../pickle/train.p")
    R = avg_dis_r(train)
    kinect_skeleton_data._save_data("../pickle/r.p", R)
    print("r.p has been generated")


def normalize_action_sequence(action_sequence, r, apply_gaussian_filter):
    """
    :param action_sequence: array of (frames, 20, 5) positions for an action sequence
    :param vector with average joint segment lengths
    :return: normalized (frames, 20, 3)
    """
    normalized_frames = []
    smoothed_action_sequence = None
    if apply_gaussian_filter:
        smoothed_action_sequence = gaussian_filter.gaussian_filter(np.array(action_sequence))[:, :, 1:]
    else:
        smoothed_action_sequence = np.array(action_sequence)[:, :, 1:]

    for frame in smoothed_action_sequence:
        norm_skele = normalize_skeleton(frame, r)
        normalized_frames.append(norm_skele)
    return normalized_frames


def get_mp_descriptors(norm_action_sequence):
    """
    :param norm_action_sequence: array of (frames, 20, 3) positions for an action sequence [[[frame, joint, x, y, z],...,]]
    :return: an mp_descriptor with time for each frame in the action_sequence
    """
    norm_action_sequence = np.array(norm_action_sequence)

    first_derivatives = first_derivative(norm_action_sequence)
    second_derivatives = second_derivative(norm_action_sequence)
    return [norm_action_sequence, first_derivatives, second_derivatives]


def format_skeleton_data(skeleton_data, apply_gaussian_filter=True):
    """
    Format kinect skeleton data to a normalized representation centered around the hip

    Parameters
    ====
    :param skeleton_data: Skeleton data
                Format: [ [ [frame #, joint #, x, y, z], ... (all joints) ] ... (all frames) ]

    Returns
    ====
    :returns tuple of (X, label)
            Format:     X = [ descriptors ... (all frames) ]
                        descriptor_joint_0 = [x, y, z, x', y', z', x'', y'', z'', frame_t]
                        descriptors = [descriptor_joint_0, ..., descriptor_joint_19]
    """
    normalized_action_sequence = normalize_action_sequence(skeleton_data, r_vector, apply_gaussian_filter)
    action_sequence_features = get_mp_descriptors(normalized_action_sequence)
    # cut off frames where derivatives cannot be calculated
    descriptors = []
    for frame_t in range(2, len(action_sequence_features[0]) - 3):
        frame_descriptors = []
        for joint in range(20):
            mp_descriptor = np.array([*action_sequence_features[0][frame_t][joint],
                             *action_sequence_features[1][frame_t][joint],
                             *action_sequence_features[2][frame_t][joint],
                              frame_t - 2])
            frame_descriptors.append(mp_descriptor)
        descriptors.append(np.array(frame_descriptors))
    return np.array(descriptors)


def format_skeleton_data_dict(skeleton_data_dict, apply_gaussian_filter=True):
    """
    Format kinect skeleton data dictionary to a normalized representation centered around the hip

    :param skeleton_data_dict: Dictionary of skeleton data
        Format: skeleton_data_dict[file_name] = [ [ [frame #, joint #, x, y, z], ... (all joints) ], ... (all frames) ]

    :return: Tuple of (X, labels)
                Format:     X = [ [ descriptors ... (all frames) ] ... (all files) ]
                            where descriptors is described in format_skeleton_data
                            labels = [ str(pose) ... (all files) ]
    """
    X = []
    labels = np.empty(shape=0)
    for file_name, action_sequence in skeleton_data_dict.items():
        labels = np.append(labels, file_to_label_dict[file_name[:3]])
        X.append(format_skeleton_data(action_sequence, apply_gaussian_filter))
    return np.array(X), labels


# find distance between 2 3D points
def distance(point1, point2):
    d = np.sqrt(np.sum(np.square(point1 - point2)))
    return d


