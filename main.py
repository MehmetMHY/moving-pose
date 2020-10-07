import get_data as gd
import Skeleton as s


train = gd.loadData("train.p")

temp = train["a04_s06_e02_skeleton_proj.txt"]

def printList(items):
    p = 0
    for i in range(len(items)):
        print(items[i])
        p = p + 1
    print("------->", p)

for key, value in train.items():
    if(key == "a04_s06_e02_skeleton_proj.txt"):
        #print(key, ' : ', value)
        printList(value)
