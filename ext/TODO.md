# Project's TODO List:
- Updated: 12-31-2020

## Tasks:

### GUI:
- [ ] Create a script that can easily setup dependencies, SkeletonBasic-D2D, and anything else needed to make the GUI work. Ideally this will be one script the user can run and it will be optimatied to work with Windows 10.
- [ ] Make ai_GUI.py work depending on what OS its beening ran on, i.e Windows 10, MacOS, or Linux.
- [ ] Add an option to the GUI that allows the user to pick which trained model they would like to use.
- [ ] (stretch goal) Get the SkeletonBasic-D2D to work on Linux. Some how get the Kinetic drivers and skeleton recognition to work on a Linux distro like Ubuntu.
- [ ] Updated GUI README after all these changes.

### Moving Pose:
- [ ] Conduct further testing and debugging on implmented moving pose method.
- [ ] Optimize code to be faster. It really lags when moving pose is applied to a recorded skeleton data. Potentially utilize the GPU.
- [ ] Improve the accuracy of the model, currently its at 68% we can get it up to 75%.

### Hardware:
- [ ] (stretch goal) Implement and test the code with other depth sensors, like a Kinetic V2.
- [ ] (stretch goal) Get the skeleton recognition part of the sensor to work with just a Camera.

### Overall Repo:
- [ ] Add the currently best trained model to the repo, look into git-lfs.
