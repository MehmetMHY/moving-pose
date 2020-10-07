import Skeleton as s
import numpy as np


# find distance between 2 3D points
def distance(point1, point2):
    d = np.sqrt(np.sum(np.square(point1 - point2)))
    return d

def avg_dis_r(data):
    bodies = np.array()
    for file_name, action_frames in data.items():
        for frame in action_frames:
            body = []
            skele = Skeleton(np.array(frame[1:]))
            for start, end in skele:
                segment = distance(start, end)
                body.append(segment)
            bodies = np.append(bodies, np.array(body))

    return np.mean(bodies, axis=0)
