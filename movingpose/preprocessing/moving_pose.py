from movingpose.preprocessing import skeleton_normalization
from movingpose.preprocessing import derivatives
import numpy as np


def normalize_action_sequence(action_sequence, r):
    """
    :param action_sequence: array of (frames, 20, 5) positions for an action sequence
    :param vector with average joint segment lengths
    :return: normalized (frames, 20, 3)
    """
    normalized_frames = []
    action_sequence = np.array(action_sequence)[:, :, 1:]
    for frame in action_sequence:
        norm_skele = skeleton_normalization.normalize_skeleton(frame, r)
        normalized_frames.append(norm_skele)
    return normalized_frames


def get_mp_descriptors(norm_action_sequence):
    """
    :param norm_action_sequence: array of (frames, 20, 5) positions for an action sequence [[[frame, joint, x, y, z],...,]]
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
                    label = str(pose)
    """
    pass


def format_skeleton_data_dict(skeleton_data_dict):
    """
    Format kinect skeleton data dictionary to a normalized representation centered around the hip

    :param skeleton_data_dict: Dictionary of skeleton data
        Format: skeleton_data_dict[file_name] = [ [ [frame #, joint #, x, y, z], ... (all joints) ], ... (all frames) ]

    :return: Tuple of (X, labels)
                Format:      X = [ [ descriptors ... (all frames) ] ... (all files) ]
                        labels = [ str(pose) ... (all files) ]
    """
    # file_to_label_dict = kinect_skeleton_data.load_pickle(file_to_label)
    # data = kinect_skeleton_data.load_pickle(data_file)
    # r = kinect_skeleton_data.load_pickle(r_file)
    # all_mp_descriptors = defaultdict(list)  # features : [list of descriptor for every frame], labels : list of labels for every frame
    #
    # for file in data.keys():
    #     print(f'creating mp for {file}')
    #     action_sequence = data[file]  # action_sequence (frames, 20, 5) array
    #     norm_sequence = normalize_action_sequence(action_sequence, r)  # norm_sequence (frames, 20, 3)
    #     sequence_mp_descriptors = get_mp_descriptors(norm_sequence)  # sequence_mp_descriptors (3, frames, 20, 3)
    #
    #     action_descriptors = []
    #     label = []
    #     # only want t where derivatives can be calculated
    #     for t in range(2, len(action_sequence) - 3):
    #             for joint in range(20):
    #                 descriptor_vector = [*sequence_mp_descriptors[0][t][joint],
    #                                     *sequence_mp_descriptors[1][t][joint],
    #                                     *sequence_mp_descriptors[2][t][joint],
    #                                     t]
    #
    #
    #                 action_descriptors.append(descriptor_vector)
    #     label = file_to_label_dict[file[:3]]
    #     all_mp_descriptors[file] = tuple([action_descriptors, label])
    #
    # print('mp generation complete')
    # return all_mp_descriptors
    pass


