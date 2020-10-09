import pickle
import time
import os

# sets any nah to 0 value
def removeNAH(data):
    for i in range(len(data)):
        for j in range(len(data[i])):
            if(str(data[i][j]) == 'nan'):
                data[i][j] = 0
    return data

# read text file into list of lists
def readFile(name):
    with open(name) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    final = []
    for i in range(len(content)):
        final.append(list(map(float, content[i].split())))
    return removeNAH(final)

# grabs all values for a certain frame
def frameOnly(frame, values):
    result = []
    for i in range(len(values)):
        if(values[i][0] == frame):
            x = values[i]
            #x.pop(0) ; x.pop(0)
            result.append(x)
    return result

# gets all file names and path to those files given a dir
def getAllDirs(type_tt):
    allFiles = os.listdir(type_tt)
    allDir = []
    for i in range(len(allFiles)):
        allDir.append(type_tt + allFiles[i])
    return allFiles, allDir

# print list
def printList(temp):
    for i in range(len(temp)):
        print(temp[i])

# create main directory for the data
#   - format: [file name : all_frames_for_a_person[frame_(1), ..., frame_(i+1)]]
def makeMainDic(data_path):
    fileNames, filePaths = getAllDirs(data_path)
    data = {}
    for i in range(len(filePaths)):
        temp = []
        get_data = readFile(str(filePaths[i]))
        lastFrame = int(get_data[len(get_data)-1][0])
        for p in range(lastFrame):
            x = frameOnly(p+1, get_data)
            temp.append(x)
        data[fileNames[i]] = temp
    return data

# save directory to a file
def saveData(filename, data):
    if(filename[len(filename)-2] == "." and filename[len(filename)-1] == "p"):
        filename = filename
    else:
        filename = str(filename + ".p")

    with open(filename, 'wb') as fp:
        pickle.dump(data, fp, protocol=pickle.HIGHEST_PROTOCOL)
    print("Saved data to file: " + filename)

# load directory from a file
def loadData(filename):
    data = {}
    with open(filename, 'rb') as fp:
        data = pickle.load(fp)
    return data

# main function
def main(train_path, test_path):
    start_time = time.time()
    print("Get test data...")
    test = makeMainDic(test_path)

    print("Get train data...")
    train = makeMainDic(train_path)

    print("Saving datas...")
    saveData("../Pickles/test.p", test)
    saveData("../Pickles/train.p", train)

    print("Program took", time.time() - start_time, "to run!")


if __name__ == "__main__":
    # paths to Test and Train data set s (this can change)
    test_path = "../Multiview_Action_3D_Dataset/dataset_full/Test/"
    train_path = "../Multiview_Action_3D_Dataset/dataset_full/Train/"

    main(train_path, test_path)