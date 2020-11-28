from movingpose.preprocessing import skeleton_normalization
from movingpose.preprocessing import derivatives
from movingpose.preprocessing.gaussian_filter import gaussian_filter
from movingpose.preprocessing.kinect_skeleton_data import load_pickle
import numpy as np

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


def normalize_action_sequence(action_sequence, r):
    """
    :param action_sequence: array of (frames, 20, 5) positions for an action sequence
    :param vector with average joint segment lengths
    :return: normalized (frames, 20, 3)
    """
    normalized_frames = []

    smoothed_action_sequence = gaussian_filter(np.array(action_sequence))[:, :, 1:]
   # action_sequence = np.array(action_sequence)[:, :, 1:]

    for frame in smoothed_action_sequence:
        norm_skele = skeleton_normalization.normalize_skeleton(frame, r)
        normalized_frames.append(norm_skele)
    return normalized_frames


def get_mp_descriptors(norm_action_sequence):
    """
    :param norm_action_sequence: array of (frames, 20, 3) positions for an action sequence [[[frame, joint, x, y, z],...,]]
    :return: an mp_descriptor with time for each frame in the action_sequence
    """
    norm_action_sequence = np.array(norm_action_sequence)

    first_derivatives = derivatives.first_derivative(norm_action_sequence)
    second_derivatives = derivatives.second_derivative(norm_action_sequence)
    return [norm_action_sequence, first_derivatives, second_derivatives]


def format_skeleton_data(skeleton_data):
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
    normalized_action_sequence = normalize_action_sequence(skeleton_data, r_vector)
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


def format_skeleton_data_dict(skeleton_data_dict):
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
        X.append(format_skeleton_data(action_sequence))
    return np.array(X), labels
