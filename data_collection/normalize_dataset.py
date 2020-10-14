# generate a dataset containing normalized points
# Data format will be same as test.p / train.p
# key names will be more descriptive than the og file names saved in norm_test.p and norm_train.p
# file key : [ [[frame, joint, x, y ,z], [frame, last_joint, x, y ,z]],[[next_frame, joint, x, y, z], ...]] ...]
# s - subject
# e - episode

import data_collection.get_data as gd
import time
import numpy as np
import data_collection.skeletonnormalization as SN
import pickle

train = gd.load_data('../pickle/train.p')
R = gd.load_data('../pickle/r.p')

def get_frame(frame, data):
    return np.array(data)[frame - 1, :, 1:]

action_data = train['a07_s04_e01_skeleton_proj.txt']

# find average time to normalize a frame
avg_normalization_time = 0

for i in range(1, len(action_data) + 1):
    start = time.time()
    frame_data = get_frame(i, action_data)
    norm_data = SN.normalize_skeleton(frame_data, R)
    end = time.time()
    normalization_time = end - start
    avg_normalization_time += normalization_time

avg_normalization_time /= len(action_data)

print(f'Average normalization of one frame took: {avg_normalization_time} seconds')
print(f'Estimated time to normalize all train data: {avg_normalization_time * 200 * 192} seconds')
# normalize all frames
# TODO getting divide by 0 error
for file in train:
    action_data = train[file][:]
    norm_frames = []
    for frame in action_data:
        frame = np.array(frame)
        norm_frame = SN.normalize_skeleton(frame[:, 1:], R)
        frame[:, 2] = norm_frame[:, 0]
        frame[:, 3] = norm_frame[:, 1]
        frame[:, 4] = norm_frame[:, 2]
        norm_frames.append(frame)
    train[file] = norm_frames

    print(f'completed file {file}')

# norm_train now saved in train
gd.save_data('../pickle/norm_train.p', train)


actions = {'a01': 'drink',
           'a02': 'eat',
           'a03': 'read-book',
           'a04': 'call-cell-phone',
           'a05': 'write-on-a-paper',
           'a06': 'use-laptop',
           'a07': 'use-vacuum-cleaner',
           'a08': 'cheer-up',
           'a09': 'sit-still',
           'a10': 'toss-paper',
           'a11': 'play-game',
           'a12': 'lie-down-on-sofa',
           'a13': 'walk',
           'a14': 'play-guitar',
           'a15': 'stand-up',
           'a16': 'sit-down'}

