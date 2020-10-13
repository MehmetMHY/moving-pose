from math import pi, sqrt, exp
import numpy as np

def printList(values):
    c = 1
    for i in values:
        print(c, i)
        c = c + 1

frame = [[0.103, -0.423, 2.320], [0.101, -0.379, 2.314], [0.108, -0.163, 2.249], [0.128, 0.025, 2.148], [-0.081, -0.223, 2.282], [-0.119, -0.426, 2.195] ,[-0.143, -0.651, 2.075] ,[-0.121, -0.755, 2.012] ,[0.258, -0.217, 2.323] ,[0.268, -0.397, 2.267] ,[0.082, -0.441, 2.052] ,[0.122, -0.477, 2.028] ,[0.012, -0.499, 2.323] ,[-0.171, -0.623, 2.102] ,[-0.181, -0.826, 2.039] ,[-0.121, -0.814, 2.076] ,[0.204, -0.494, 2.339] ,[0.305, -0.643, 2.083] ,[0.286, -0.788, 2.114] ,[0.273, -0.854, 2.087]]

print("-----[ BEFORE ]-----")
printList(frame)
print()

# 5x1 Gaussian Filter
def gauss(n, sigma):
    r = range(-int(n/2),int(n/2)+1)
    return [1 / (sigma * sqrt(2*pi)) * exp(-float(x)**2/(2*sigma**2)) for x in r]

o = 1
n = 5

filter = gauss(n, o)
temp = np.vstack(filter)

print(temp*frame[0])

