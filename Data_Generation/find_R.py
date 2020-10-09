import sys
sys.path.append('..')
import Skeleton as s
import numpy as np
from numpy import linalg as LA
from Data_Generation import get_data as gd


# find distance between 2 3D points
def distance(point1, point2):
    d = np.sqrt(np.sum(np.square(point1 - point2)))
    return d


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
    return R / LA.norm(R)

# generates R using the training data
def generate_R():
    train = gd.loadData("../Pickles/train.p")
    R = avg_dis_r(train)
    gd.saveData("../Pickles/R.p", R)
    print("R.p has been generated")
