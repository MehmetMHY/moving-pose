from tkinter import messagebox as mb
from functools import partial
import tkinter.font as font
from tkinter import *
import tkinter as tk
import webbrowser
import time
import ctypes
import os
from movingpose.estimator import classifiers
from movingpose.estimator import neighbors
from movingpose.preprocessing import kinect_skeleton_data
from movingpose.preprocessing import moving_pose

# add whitespace between UI's images, labels, or buttons
def load_classifier(cache_path, parameters_path):
    parameters = classifiers.load_pickle(parameters_path)
    pose_params = parameters['action_classifier_params']['nearest_pose_estimator']
    classifier_params = parameters['action_classifier_params']

    nearest_pose_estimator = neighbors.NearestPoses(
        n_neighbors=pose_params['n_neighbors'],
        n_training_neighbors=['n_training_neighbors'],
        alpha=pose_params['alpha'],
        beta=pose_params['beta'],
        kappa=pose_params['kappa']
    )

    action_classifier = classifiers.ActionClassifier(
        nearest_pose_estimator=nearest_pose_estimator,
        theta=classifier_params['theta'],
        n=classifier_params['n']
    )

    action_classifier.fit(cache_path=cache_path)
    return action_classifier


model = load_classifier('pickle/c7f7094d/action_classifier_cache-2000.p','pickle/c7f7094d/prediction-[n=50_theta=0.3_ne\
arest_pose_estimator=[alpha=0.75_beta=0.6_kappa=10_n_neighbors=10_n_training_neighbors=2000]].p')


#
def format_data():
    raw_data = kinect_skeleton_data.parse_txt('ext/data.txt')
    normalized_descriptors = moving_pose.format_skeleton_data(raw_data)
    return normalized_descriptors


def add_whitespace(amount):
    whitespaceFont = font.Font(family='Helvetica', size=5)
    for i in range(amount):
        Label(root, text=' ', font=whitespaceFont).pack(fill=tk.BOTH)


# open project's GitHub web page
# TODO delete
def openREADME():
    webbrowser.open('https://en.wikipedia.org/wiki/Kinect') # TODO, link main project repo when made public

# open "Moving Pose" research paper web page
# TODO delete
def openPaper():
    webbrowser.open('https://openaccess.thecvf.com/content_iccv_2013/papers/Zanfir_The_Moving_Pose_2013_ICCV_paper.pdf')

# Link: https://stackoverflow.com/questions/1265665/how-can-i-check-if-a-string-represents-an-int-without-using-try-except
# check if a string is an int or not

def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


# print list indexes line by line
def printList(data):
    for i in data:
        print(i)


# read textfile into a list
def read_text_file(name):
    with open(name) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content

# set textfile to stop C++ code from recording to a text file
def reset():
    file = open("record_frame_count.txt", "w+")
    file.write("DONE")
    results.config(text="...")
    file.close()

# create prediction with moving pose
def predict():
    global model
    normalized_data = format_data()
    prediction = model.predict(normalized_data)
    print(prediction)
    results.config(text=prediction[0])

# # comminucate between python and C++ code
# def process_frame_count(frame_count):
#     global filePath
#     if(is_int(frame_count.get()) == True):
#         state = readTextFile(filePath)
#         state = str(state[0])
#         if(state == "DONE"):
#             file = open(filePath, "w+")
#             file.write(str(frame_count.get()))
#             results.config(text = "LOADING")
#         elif(state == "DONE-RECORDING"):
#             #mb.showinfo("Result", "Running!")
#             results.config(text = "Processing...")
#             reset()
#             prediction()
#         else:
#             mb.showerror("Error", "Currently Recording, Please Wait!")
#     else:
#         mb.showerror("Error", "Please enter frame count as an int! Try Again!")


def start_recording():
    file = open("record_frame_count.txt", "w+")
    file.write("100000")
    results.config(text = "LOADING...")
    file.close()


def stop_process():
    file = open("record_frame_count.txt", "w+")
    file.write("STOP")
    file.close()
    time.sleep(3)
    reset()
    predict()


# clean UI's resolution for higher resolution monitors (Windows 10 only)
ctypes.windll.shcore.SetProcessDpiAwareness(2)

# setup tkinter object
root = Tk()

# setup text fonts in UI
defaultOptionsFont = font.Font(family='Helvetica', size=20)
defaultLabelFont = font.Font(family='Helvetica', size=20)
defaultButtonFont = font.Font(family='Helvetica', size=15)
resultsFont = font.Font(family='Helvetica', size=18)

# setup UI colors
bgColor = "white"
bgButton = "ghost white"

# setup UI dimension
dimensions = "550x1230"

# setup "results" label
#   - this will be used to display predictions from moving pose
results = Label(root, text="...", font=resultsFont)
filePath = "record_frame_count.txt"

### GUI Windows Setups

# setup UI shape
root.title('SRC-20')
root.configure(background=bgColor)
root.resizable(width=False, height=False)
root.geometry(dimensions)

# menu setup for README & MovingPose
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label='README', command=openREADME)
menu.add_cascade(label='MovingPose', command=openPaper)

# UI's top image icon
photoIcon = PhotoImage(file = r"GUI_Icon.png")
Button(root, image = photoIcon, highlightbackground=bgColor).pack(side = TOP)

# # setup FRAME COUNT label
# Label(root, text='Frame Count', font=defaultLabelFont, bg='lightgreen').pack(fill=tk.BOTH)
# addWhitespace(1)

# # setup UI's FRAME text input
# frame_count = StringVar()
# Entry(root, textvariable=frame_count, font=defaultLabelFont).pack(fill=tk.BOTH)
# process_frame_count = partial(process_frame_count, frame_count)
# addWhitespace(1)

resultsLabelColor = 'light green'
Label(root, text='Start Recording', font=defaultLabelFont, bg=resultsLabelColor).pack(fill=tk.BOTH)
add_whitespace(1)

# setup UI's RECORD/PROCESS button
tk.Button(root, text='START', width=350, command=start_recording, highlightbackground=bgColor, font=defaultButtonFont, bg=bgButton).pack()
add_whitespace(1)

resultsLabelColor = 'orange red'
Label(root, text='Start Recording', font=defaultLabelFont, bg=resultsLabelColor).pack(fill=tk.BOTH)
add_whitespace(1)

# setup UI's RECORD/PROCESS button
tk.Button(root, text='STOP/Process', width=350, command=stop_process, highlightbackground=bgColor, font=defaultButtonFont, bg=bgButton).pack()
add_whitespace(1)

# setup UI's RESULTS label
resultsLabelColor = 'light blue'
Label(root, text='Results', font=defaultLabelFont, bg=resultsLabelColor).pack(fill=tk.BOTH)
add_whitespace(1)

# setup UI's result label
results.pack(fill=tk.BOTH)
add_whitespace(2)

# setup UI's RESET label
resetLabelColor = 'red'
Label(root, text='RESET', font=defaultLabelFont, bg=resetLabelColor).pack(fill=tk.BOTH)
add_whitespace(1)

# setup UI's RESET button
tk.Button(root, text='<*_*>', width=350, command=reset, highlightbackground="red", font=defaultButtonFont, bg=bgButton).pack()
add_whitespace(2)

# main tkinter loop
root.mainloop()
