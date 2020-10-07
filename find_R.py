import Skeleton as s
import numpy as np


# find distance between 2 3D points
def distance(point1, point2):
    d = np.sqrt(np.sum(np.square(point1 - point2)))
    return d

<<<<<<< HEAD
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
=======

def avg_dis_r(data):
    final = []
    for person, frames_poses in data.items():
        people = []
        for i in range(len(frames_poses)):
            frames = []
            for j in range(len(start_to_end)):
                start = frames_poses[i][start_to_end[j][0]-1][2:]
                end = frames_poses[i][start_to_end[j][1]-1][2:]
                frames.append(distance(start, end))
            people.append(frames)
        people = np.array(people)
        final.append(np.mean(people, axis=0))
>>>>>>> 68985dd733f8351cb8ab0d59795b46875b544c47

    return np.mean(bodies, axis=0)
