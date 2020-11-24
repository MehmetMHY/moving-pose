# Windows Application Element
- Date: 10-13-2020

![wnmf](https://user-images.githubusercontent.com/15916367/95893287-00aa5700-0d45-11eb-9cb9-14601c9545dd.jpg)

## About:
- Sadly, our Kinetc V1 sensor works best in Windows. This is due to the kinetic being a Microsoft product and the fact that its drivers are close-sourced. 
- An attempt was made to get the Kinetic V1 sensor to work correctly with Ubuntu 20.04 and Ubuntu 16.04, but though the depth data was successfully read. The skeleton joint points were not as much of the code for this was outdated and certain drivers were no longer supported for any of the non-EOL Ubuntu verisons.
- Because of this, the first goal was to find a way to export the data from the Kinetic from Windows 10 Ubuntu but after consideration, we decided to implment everything into Windows to avoid any major lags.

## Basic Setup:
- To see the basic setup, please view the README in kinect_skeleton_data_code/

## Main Goal:
- Get the Python code to work with Windows and C++:
	- Use Docker or Conda
- Get C++ to compicate with Python and vise versa
	- Use Cython
- Modify the SkeletonBasic-D2D code's GUI for this project
	- Understand the code, and create new GUI in C++
	- (if C++ fails) create a new GUI in Python (Kiviy)
- Make the whole project and exe file


