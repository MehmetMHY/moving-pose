# Project Export Kinetic V1 Skeleton Data
- Date: 9-27-2020

## Hardware:
- Kinetic V1
- PC (Windows 10)
- Visual Studio 2019

## Software:
- Kinect for Windows runtime v1.8 (drivers)
- Kinect Windows Developer Toolkit v1.8.0

## About:
- The main goal of this project is to effectivly export the skeleton data from the,
kinetic sensor to a local webserver that can be acccessed by any computer in the,
network. So ideally, the data will come from Windows 10 but the computing for,
kinetic based projects will be done on Linux systems.

## Credits:
- The main way the data is being calculated and read, is though one of Microsoft's,
"Kinect Developer Toolkit v1.8.0 Resources & Samples" which is a grouping of many,
simple kinetic based projects that are written in C#, C++, etc.
- The Sample used for this project is called "Skeleton Basic-D2D", which demonstrates,
the SkeletonStream data from the kinetic by displaying it in a GUI. The code for this,
was provided and is used. I was able to get it to compile in Visual Studio 2019.
- This is not "my" project, due to poor documatation and how old the Kinetic V1 is,
I found this method of using this Sample code and exporting it to a web server,
to be the most successful so far. So this is not my project, rather I am building,
a little bit on top of all the work done by the open source community and Microsoft.

## Ideas:
- Send data from Windows 10 to Linux machine though a web server
- Send data from Windows 10 to Linux machine though ssh

## Goals:
1) Get Kinetic V1 and make sure it works with Ubuntu or Windows		[X]
2) Read skeleton tracking data from Kintic Sensor		[X]
3) Find a way to export the data:
	- get it to work on Ubuntu/Linux	(FAILED)
	- get it to work on Windows 10
		- send data from Windows 10 to web server
		- have linux system read data from web server

