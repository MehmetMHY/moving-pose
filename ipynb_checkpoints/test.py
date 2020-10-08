from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import sys ; sys.path.append('../')
from Skeleton import Skeleton
import SkeletonNormalization as SN
import get_data as gd
from find_R import *

def get_frame(frame, data):
    return np.array(data)[frame - 1,:,1:]

def graph_it(xs_norm, ys_norm, zs_norm):
    colors = ['blue' for i in range(20)]
    colors[0] = 'red'  # hip is red
    colors[7] = 'green'  # hands and feet are green
    colors[11] = 'green'
    colors[15] = 'green'
    colors[19] = 'green'
    colors[3] = 'black' # head is black
    xs, ys, zs = frame_data[:, 1], frame_data[:, 2], frame_data[:, 3]
    fig = plt.figure()
    ax = fig.add_subplot(1, 2, 1, projection='3d')
    scatter_1 = ax.scatter(xs, ys, zs, color=colors)
    ax = fig.add_subplot(1, 2, 2, projection='3d')
    scatter_2 = ax.scatter(xs_norm, ys_norm, zs_norm, color=colors)
    plt.show()


train = gd.loadData('../train.p')
action_data = train["a08_s01_e01_skeleton_proj.txt"]

frame_data = get_frame(1, action_data)
skele = Skeleton(frame_data)

R = list(gd.loadData("../R.p"))
norm_skele = SN.normalize_skeleton(frame_data, R)
xs_norm, ys_norm, zs_norm = norm_skele[:,0], norm_skele[:,1], norm_skele[:,2]

print(xs_norm)
print()
print(ys_norm)
print()
print(zs_norm)
