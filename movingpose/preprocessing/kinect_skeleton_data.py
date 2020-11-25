import pickle
import time
import os


def pickle_dir(save_path, data_dir):
    """
    Pickle directory of formatted skeleton data text files using kinect_skeleton_data#parse_dir

    Parameters
    ====
    :param save_path: Save location path
    :param data_dir: Directory of kinect skeleton data
    """
    start_time = time.time()

    print("Pickling skeleton data...")
    mp_files = parse_dir(data_dir)

    print("Saving data...")
    _save_data(save_path, mp_files)

    print("Program took", time.time() - start_time, "to run!")


def parse_dir(skeleton_data_dir):
    """
    Save directory of formatted skeleton data text files to a dictionary

    Parameters
    ====
    :param skeleton_data_dir: Directory of formatted kinect skeleton data text files

    Return
    ====
    :return Dictionary of formatted skeleton data
        Format: data[file_name] = [ [ [frame #, joint #, x, y, z], ... (all joints) ], ... (all frames) ]
    """
    file_names, file_paths = _get_all_dirs(skeleton_data_dir)
    data = {}
    for i, file_path in enumerate(file_paths):
        data[file_names[i]] = parse_txt(str(file_path))
    return data


def parse_txt(file_path):
    """
    Parse formatted skeleton data text file into list of raw descriptors

    Parameters
    ====
    :param file_path: Text file location

    Returns
    ====
    :return List of raw descriptors
                [ [ [frame #, joint #, x, y, z], ... (all joints) ] ... (all frames)]
    """
    with open(file_path) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    raw_descriptors = []
    for line in lines:
        raw_descriptors.append(list(map(float, line.split())))

    mildly_formatted_descriptor = []
    last_frame = int(raw_descriptors[-1][0])
    for frame in range(last_frame):
        x = _frame_only(frame + 1, raw_descriptors)
        mildly_formatted_descriptor.append(x)

    return remove_nan(mildly_formatted_descriptor)


def load_pickle(filename):
    """
    Load formatted skeleton data from pickle file
    """
    with open(filename, 'rb') as fp:
        data = pickle.load(fp)
    return data


def remove_nan(values):
    """
    Replaces all 'nan' value in a list with '0'
    """
    for i in range(len(values)):
        for j in range(len(values[i])):
            if str(values[i][j]) == 'nan':
                values[i][j] = 0
    return values


def _save_data(filename, data):
    """
    Save formatted skeleton data to a pickle file
    """
    if filename[-2:] == ".p":
        filename = filename
    else:
        filename = str(filename + ".p")

    with open(filename, 'wb') as fp:
        pickle.dump(data, fp, protocol=pickle.HIGHEST_PROTOCOL)
    print("Saved data to file: " + filename)


def _frame_only(frame, skeleton_data):
    """
    Save only one frame from skeleton data
    """
    result = []
    for raw_descriptor in skeleton_data:
        if raw_descriptor[0] == frame:
            result.append(raw_descriptor)
    return result


def _get_all_dirs(type_tt):
    """
    Retrieve all files within a directory

    Parameters
    ====
    :param type_tt: Directory

    Returns
    ====
    :return Tuple of (file_names, file_paths)
    """
    file_names = os.listdir(type_tt)
    file_paths = []
    for i in range(len(file_names)):
        file_paths.append(type_tt + file_names[i])
    return file_names, file_paths


if __name__ == "__main__":
    # Path to multiview action directory
    pickle_dir("../../pickle/multiview.p", "../../ext/dataset/multiview_action/")
