import time

from .globalRobotChecking import GlobalRobotChecking

from urbasic import ISCoin
from math import radians
from urbasic import Joint6D
import json

# function to read a simulation json and read it to control the robot
def readJson(path):
	points = []
	with open(path, 'r') as file:
		data = json.load(file)["modTraj"]
		for i in data:
			points.append(i['positions'])
	return points
# Create a new ISCoin object
# UR3e1 IP (closest to window): 10.30.5.158
# UR3e2 IP: 10.30.5.159
iscoin = ISCoin(host="10.30.5.159", opened_gripper_size_mm=40)

interval = 0.1 # in case of need you cam change the interval


# Reset any potential error
iscoin.robot_control.reset_error()

jsonPath = "security/trajectories_test/traj_test_collision_gripper.json"
waypoints = readJson(jsonPath)

checking_task = GlobalRobotChecking(True, True,interval, iscoin=iscoin)  #change with the first angle detected by the robot
checking_task.start()  # Start the task
# for i in waypoints:

# 	jo = Joint6D.createFromRadList(i)
# 	if not checking_task.check:
# 		print("Illegal movement detected, stopping the robot.")
# 		break

# 	#print(f'Joints are at {"iscoin.robot_control.get_actual_joint_positions()"} - going to {jo}')
# 	iscoin.robot_control.movej(jo, a = radians(5), v = radians(5))
	
# checking_task.stop()  # Stop the task """
while True: 
	time.sleep(0.1)