# Team Nestlé CSCI470 Project

<img width="350" alt="3" src="https://user-images.githubusercontent.com/15916367/94550311-c1dab400-0210-11eb-92df-8e0064d639de.jpg">

## Members:
- Andrew Darling
- Eric Hayes
- Mehmet Yilmaz

## About:
- This is the Fall 2020 CSCI470 Semester Project
- We are implmenting the following research paper for this project: https://openaccess.thecvf.com/content_iccv_2013/papers/Zanfir_The_Moving_Pose_2013_ICCV_paper.pdf

## Multiview Action 3D Dataset Action IDs:
<img width="701" alt="3" src="https://user-images.githubusercontent.com/15916367/85251734-4bf7cd00-b417-11ea-8003-de9340da3c0c.png">

## Project:
- Topic Area: Supervised Learning, Binary Classification, Support Vector Model (SVM)
- Project Name: Binary Action Classifier
- Problem Statement:  Identify human actions from static wireframe poses
- Proposed Solution: Using wireframe skeleton data for different poses, our minimum viable product is a machine learning algorithm that recognizes if a skeleton is in a pose or not in that pose. A stretch goal will be identifying one of multiple different poses.
- Data: We will be using the Northwestern-UCLA Multiview Action 3D Dataset. The dataset contains information from multiple people performing 10 different types of actions. For every person performing an action, the dataset contains a CSV file where every line contains 5 values: the frame, joint id (20 joints total), x-pos, y-pos, z-pos. We plan on cleaning the data by selecting the most relevant frame and using the x, y, and z-positions of each joint to calculate features that will predict the pose someone is striking.

## Great Sources:
1) http://inside.mines.edu/~hzhang/Courses/CSCI473-573/schedule.html
2) http://inside.mines.edu/~hzhang/Courses/CSCI473-573/assignment.html (project 3)
