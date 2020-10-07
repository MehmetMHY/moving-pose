import get_data as gd
import Skeleton as s
import numpy as np
import math

# find distance between 2 3D points
def distance(point1, point2):
    x1 = point1[0] ; y1 = point1[1] ; z1 = point1[1]
    x2 = point2[0] ; y2 = point2[1] ; z2 = point2[2]

    d = math.sqrt(math.pow(x2 - x1, 2) +
                math.pow(y2 - y1, 2) +
                math.pow(z2 - z1, 2)* 1.0)
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
