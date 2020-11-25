from movingpose.logic import iterators as s
from movingpose.preprocessing import kinect_skeleton_data as gd
import numpy as np
from numpy import linalg as LA


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
def generate_r():
    train = gd.load_pickle("../pickle/train.p")
    R = avg_dis_r(train)
    gd._save_data("../pickle/r.p", R)
    print("r.p has been generated")

