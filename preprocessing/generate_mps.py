import preprocessing.get_data as gd
import preprocessing.skeleton_normalization as sn
import preprocessing.derivatives as dvts
import numpy as np
from collections import defaultdict


def normalize_action_sequence(action_sequence, r):
    """
    :param action_sequence: array of (frames, 20, 5) positions for an action sequence
    :param vector with average joint segment lengths
    :return: normalized (frames, 20, 3)
    """
    normalized_frames = []
    action_sequence = np.array(action_sequence)[:, :, 1:]
    for frame in action_sequence:
        norm_skele = sn.normalize_skeleton(frame, r)
        normalized_frames.append(norm_skele)
    return normalized_frames


def get_mp_descriptors(norm_action_sequence):
    """
    :param norm_action_sequence: array of (frames, 20, 5) positions for an action sequence [[[frame, joint, x, y, z],...,]]
    :return: an mp_descriptor with time for each frame in the action_sequence
    """
    norm_action_sequence = np.array(norm_action_sequence)
    first_derivatives = dvts.first_derivative(norm_action_sequence)
    second_derivatives = dvts.second_derivative(norm_action_sequence)
    return [norm_action_sequence, first_derivatives, second_derivatives]


def generate_mps(data_file, file_to_label='../../pickle/file_to_label.p', r_file='../../pickle/r.p'):
    """
    :param data_file:  name name of file to get data from (pickle)
    :param file_to_label: path to file with conversion from filename to label
    :return: None
    """
    file_to_label_dict = gd.load_data(file_to_label)
    data = gd.load_data(data_file)
    r = gd.load_data(r_file)
    all_mp_descriptors = defaultdict(list)  # features : [list of descriptor for every frame], labels : list of labels for every frame

    for file in data.keys():
        print(f'creating mp for {file}')
        action_sequence = data[file]  # action_sequence (frames, 20, 5) array
        norm_sequence = normalize_action_sequence(action_sequence, r)  # norm_sequence (frames, 20, 3)
        sequence_mp_descriptors = get_mp_descriptors(norm_sequence)  # sequence_mp_descriptors (3, frames, 20, 3)

        action_descriptors = []
        label = []
        # only want t where derivatives can be calculated
        for t in range(2, len(action_sequence) - 3):
                for joint in range(20):
                    descriptor_vector = [*sequence_mp_descriptors[0][t][joint],
                                        *sequence_mp_descriptors[1][t][joint],
                                        *sequence_mp_descriptors[2][t][joint],
                                        t]


                    action_descriptors.append(descriptor_vector)
        label = file_to_label_dict[file[:3]]
        all_mp_descriptors[file] = tuple([action_descriptors, label])

    print('mp generation complete')
    return all_mp_descriptors


