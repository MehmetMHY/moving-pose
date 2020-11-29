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


--------

# Project Export Kinect V1 Skeleton Data
- Date: 9-27-2020

## Disclaimer:
- This code was provided by Microsoft's Kinect V1.8 ToolKit.
- This code will mainly be used to get and send skeleton data from the Kinect Sensor.

## Hardware:
- Kinect V1
- PC (Windows 10)
- Visual Studio 2019

## Software:
- Kinect for Windows runtime v1.8 (drivers)
- Kinect Windows Developer Toolkit v1.8.0

## Installs:
- Kinect v1.8 drivers: https://www.microsoft.com/en-us/download/details.aspx?id=40277
- Kinect v1.8 toolKit: https://www.microsoft.com/en-us/download/details.aspx?id=40276
- Visual Studio 2019:  https://visualstudio.microsoft.com/downloads/

## About:
- The main goal of this project is to effectivly export the skeleton data from the,
Kinect sensor to a local webserver that can be acccessed by any computer in the,
network. So ideally, the data will come from Windows 10 but the computing for,
Kinect based projects will be done on Linux systems.

## Credits:
- The main way the data is being calculated and read, is though one of Microsoft's,
"Kinect Developer Toolkit v1.8.0 Resources & Samples" which is a grouping of many,
simple Kinect based projects that are written in C#, C++, etc.
- The Sample used for this project is called "Skeleton Basic-D2D", which demonstrates,
the SkeletonStream data from the Kinect by displaying it in a GUI. The code for this,
was provided and is used. I was able to get it to compile in Visual Studio 2019.
- This is not "my" project, due to poor documatation and how old the Kinect V1 is,
I found this method of using this Sample code and exporting it to a web server,
to be the most successful so far. So this is not my project, rather I am building,
a little bit on top of all the work done by the open source community and Microsoft.

## Ideas:
- Send data from Windows 10 to Linux machine though a web server
- Send data from Windows 10 to Linux machine though ssh

## Goals:
- Get Kinect V1 and make sure it works with Ubuntu or Windows		[X]
- Read skeleton tracking data from Kintic Sensor		[X]
- Find a way to export the data:
	- get it to work on Ubuntu/Linux	(FAILED)
	- get it to work on Windows 10
		- send data from Windows 10 to web server
		- have linux system read data from web server




