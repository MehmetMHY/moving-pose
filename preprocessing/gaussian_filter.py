import numpy as np
import cv2

# create gaussian filter kernel matrix
def create_kernel(o, n):
     return list(cv2.getGaussianKernel(ksize=n,sigma=o).T[0])

# apply gaussian filter to 1 action of the skeleton data
# notes:
#   - input:  skeleton data for 1 action (x, 20, 5)
#   - output: skeleton data with GF applied (x, 20, 5)
#   - using GF does corrupt each frame's label and joint number,
#     this will we accounted for during training.
def GF(data):
    o = 1
    n = 5

    kernel = create_kernel(o, n)

    frame = list(data.copy())

    temp = []
    for i in range(len(frame)-n):
        ans = []
        ans.append(frame[i])
        ans.append(frame[i+1])
        ans.append(frame[i+2])
        ans.append(frame[i+3])
        ans.append(frame[i+4])
        temp.append(ans)
    temp = np.array(temp)

    def finalize(x):
        for i in range(len(x)): #1-5
            k = kernel[i]
            x[i] = x[i]*k
        return sum(x)

    final = []
    for i in range(len(temp)):
        final.append(finalize(temp[i]))

    for i in range(n):
        final.append(data[(len(data)-1)-i])

    return final


