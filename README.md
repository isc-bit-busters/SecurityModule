[![codecov](https://codecov.io/gh/6figuress/SecurityModule/graph/badge.svg?token=HWDLANEU4D)](https://codecov.io/gh/6figuress/SecurityModule)
![Test status](https://github.com/6figuress/SecurityModule/actions/workflows/main.yml/badge.svg)

# SecurityModule

## Overview

SecurityModule is a project aimed at ensuring the safety and collision detection of robotic arms. It includes various functionalities to check for collisions within the robot's own structure, with the ground, and within a defined working area based on given angles and configurations.

## Features

- **Collision Detection**: Detect if any part of the robotic arm collides with another part of itself.
- **Ground Collision Detection**: Detect if any part of the robotic arm is too close to the ground.
- **Working Area Checking**: Ensure that the robotic arm stays within a predefined working area.
- **Forward Kinematics**: Calculate the coordinates of the robot's joints based on given angles.
- **Angle Variation Checking**: Ensure that the variation of robot's joints angle is not too big.
- **Manual Checking** : Filter the snon valid olutions obtained by inverse kinematics.  
- **Real-Time Checking**: Perform real-time checking of the robot's position and angles to ensure safety.

- **Unittest** : To test the functionality listed above
## Installation

To install the SecurityModule

uv add git+https://github.com/6figuress/SecurityModule.git

To update changes:

uv sync -U

## Usage

Once installed, in order to integrate the safety module in real time, all we need to do is call the main class **globalRobotChecking** as done in the file **realTimeCheckingExample.py**. To initialise it, all we need to do is set the starting angles, the interval in which we wish to repeat the safety checks and an instance of the arm control library that will allow us to acquire the real time data
For manual checking, simply use the class validateRobotChecking which takes a list of incoming angles an example of how to use it is given in the file **manualExample.py**

