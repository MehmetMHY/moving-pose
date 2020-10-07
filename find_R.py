import get_data as gd
import Skeleton as s
import numpy as np
import math

def printList(items):
    p = 0
    for i in range(len(items)):
        print(items[i])

# find distance between 2 3D points
def distance(point1, point2):
    x1 = point1[0] ; y1 = point1[1] ; z1 = point1[1]
    x2 = point2[0] ; y2 = point2[1] ; z2 = point2[2]

    d = math.sqrt(math.pow(x2 - x1, 2) +
                math.pow(y2 - y1, 2) +
                math.pow(z2 - z1, 2)* 1.0)
    return d

def avg_dis_r(data, start_to_end=[(1, 13), (1, 2), (1, 17), (13, 14), (2, 3), (17, 18), (14, 15), (3, 5), (3, 4), (3, 9), (18, 19), (15, 16), (5, 6), (9, 10), (19, 20), (6, 7), (10, 11), (7, 8), (11, 12)]):
    final = []
    for key, value in data.items():
        person = []
        for i in range(len(value)):
            frames = []
            for j in range(len(start_to_end)):
                p1 = start_to_end[j][0]-1
                p2 = start_to_end[j][1]-1
                f1 = value[i][p1][2:]
                f2 = value[i][p2][2:]
                frames.append(distance(f1, f2))
            person.append(frames)
        person = np.array(person)
        final.append(np.mean(person, axis=0))

    final = np.array(final)
    return np.mean(final, axis=0)
