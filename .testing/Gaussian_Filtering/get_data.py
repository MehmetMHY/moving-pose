import pickle
import time
import os


# sets any nah to 0 value
def remove_nah(data):
    for i in range(len(data)):
        for j in range(len(data[i])):
            if str(data[i][j]) == 'nan':
                data[i][j] = 0
    return data


# read text file into list of lists
def read_file(name):
    with open(name) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    final = []
    for i in range(len(content)):
        final.append(list(map(float, content[i].split())))
    return remove_nah(final)


# grabs all values for a certain frame
def frame_only(frame, values):
    result = []
    for i in range(len(values)):
        if values[i][0] == frame:
            x = values[i]
            #x.pop(0) ; x.pop(0)
            result.append(x)
    return result


# gets all file names and path to those files given a dir
def get_all_dirs(type_tt):
    all_files = os.listdir(type_tt)
    all_dir = []
    for i in range(len(all_files)):
        all_dir.append(type_tt + all_files[i])
    return all_files, all_dir


# print list
def print_list(temp):
    for i in range(len(temp)):
        print(temp[i])


# create main directory for the data
#   - format: [file name : all_frames_for_a_person[frame_(1), ..., frame_(i+1)]]
def make_main_dir(data_path):
    file_names, file_paths = get_all_dirs(data_path)
    data = {}
    for i in range(len(file_paths)):
        temp = []
        get_data = read_file(str(file_paths[i]))
        last_frame = int(get_data[len(get_data)-1][0])
        for p in range(last_frame):
            x = frame_only(p + 1, get_data)
            temp.append(x)
        data[file_names[i]] = temp
    return data


# save directory to a file
def save_data(filename, data):
    if filename[-2:] == ".p":
        filename = filename
    else:
        filename = str(filename + ".p")

    with open(filename, 'wb') as fp:
        pickle.dump(data, fp, protocol=pickle.HIGHEST_PROTOCOL)
    print("Saved data to file: " + filename)


# load directory from a file
def load_data(filename):
    data = {}
    with open(filename, 'rb') as fp:
        data = pickle.load(fp)
    return data


# main function
def main(train_path, test_path):
    start_time = time.time()
    print("Get test data...")
    test = make_main_dir(test_path)

    print("Get train data...")
    train = make_main_dir(train_path)

    print("Saving datas...")
    save_data("../pickle/test.p", test)
    save_data("../pickle/train.p", train)

    print("Program took", time.time() - start_time, "to run!")


if __name__ == "__main__":
    # paths to Test and Train data sets (this can change)
    test_path = "../ext/dataset/multiview_action/Test/"
    train_path = "../ext/dataset/multiview_action/Train/"

    main(train_path, test_path)