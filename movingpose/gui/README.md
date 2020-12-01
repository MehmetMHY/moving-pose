# Windows Application Element
- Date: 11-29-2020

![kta-disclaimer-1024x683](https://user-images.githubusercontent.com/15916367/100694256-ead01000-334b-11eb-82ac-a208e3c46726.png)

## Disclaimer:
- We used Microsoft's Kinect V1.8 ToolKit.
- From Kinect V1.8 ToolKit, we used and modified the SkeletonBasics-D2D C++ example code to receive the skeleton data from the Kinect Sensor as well as display the skeleton data in a nice GUI. 
- The SkeletonBasics-D2D code is NOT ours, it is owned by Microsoft. We only modified it for our project which is only used for educational proposes.

## About:
- For this project, we used a Xbox 360 Kinetic v1.18 sensor as well as a Kinetic to USB converter.
- The main data we are extracting from the Kinetic is the skeleton joint dataset.
- A Python GUI script is used to manage how many frames the kinetic sensors collects as well as process those frames into the Moving Pose algorithm.
- The Python and C++ script "communicate" with each other though one text file.

## Hardware:
- Xbox 360 Kinect Sensor v1.8
- Kinect Sensor to USB Converter
- PC (Windows 10)

## Software:
- Windows 10
- Kinect for Windows runtime v1.8 (drivers)
- Kinect Windows Developer Toolkit v1.8.0
- Visual Studio 2019 & VS19 C++ Add-On
- Python3
- Pip3
- "all the modules/packages used in Moving Pose code"

## Basic Setup:
- 1) Make sure you are running Windows 10
- 2) Install Kinect Drivers:
		- Kinect v1.8 drivers: https://www.microsoft.com/en-us/download/details.aspx?id=40277
		- Kinect v1.8 toolKit: https://www.microsoft.com/en-us/download/details.aspx?id=40276
- 3) Install Visual Studio 2019 (VS19):  https://visualstudio.microsoft.com/downloads/
		- Make sure you install any C++ add-ons if need be.
- 4) Open SkeletonBasics-D2D/ in VS19
- 5) Click on SkeletonBasics-D2D.sln
- 6) Hit VS19's "Debug" button and the code should run.
		- Go infront of the kinetic sensor and see if you can see your skeleton.
- 7) Close Debug mode and VS19
- 8) Go into modifications/ and move SkeletonBasics.cpp into SkeletonBasics-D2D/. Have it replace the original SkeletonBasics.cpp file.
- 9) Go back to modifications/ and move every other file into SkeletonBasics-D2D/Debug/
- 10) Make sure to install Python3 on Windows 10: https://www.python.org/downloads/
- 11) Repeat Step 4 again
- 12) Run the ai_GUI.py file in SkeletonBasics-D2D/Debug/
- 13) Repeat Step 6
- 14) There you go, you can now use the UI for this project.

## Credits:
- The main way the data is being calculated and read, is though one of Microsoft's,
"Kinect Developer Toolkit v1.8.0 Resources & Samples" which is a grouping of many,
simple Kinect based projects that are written in C#, C++, etc.
- The Sample used for this project is called "Skeleton Basic-D2D", which demonstrates,
the SkeletonStream data from the Kinect by displaying it in a GUI. The code for this,
was provided and is used. I was able to get it to compile in Visual Studio 2019.




