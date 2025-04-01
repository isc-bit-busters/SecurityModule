import time
import numpy as np
import pybullet as p
import pybullet_data

from .forwardKinematics import ForwardKinematic

import plotly.graph_objects as go

from urbasic import ISCoin, Joint6D




class RobotCollisionCheck :
    def __init__(self, gui=True, logs =True):
        self.logs =logs
        self.gui = gui
        if gui:
            p.connect(p.GUI)
        else:
            p.connect(p.DIRECT)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        self.robot_id = p.loadURDF("security/iscoin_azz.urdf", useFixedBase=True, flags=p.URDF_USE_SELF_COLLISION)
        self.FPS = 60
        self.time_step = 1 /  self.FPS 
        p.setTimeStep(self.time_step)
        self.nim_joints = p.getNumJoints(self.robot_id)
        self.ground_id = p.loadURDF("plane.urdf", basePosition=[0, 0, 0])
        self.penJoint = 11

        self.mapping = {0: 2, 1: 3, 2: 4, 3: 5, 4: 6, 5: 7}

    


    def _isArrived(self,targetAngles, tolerance=0.01):
        joint_positions = [p.getJointState(self.robot_id, self.mapping[i])[0] for i in self.mapping]

        for i, a in enumerate(joint_positions):
            if abs(targetAngles[i] - a) > tolerance:
                return False
        return True
    def check_working_area(self):
        # working area definition
        x_min = -0.31
        x_max = 0.62
    
        y_min = 0
        y_max = 0.62
    
        z_min = -0.0
        z_max = 0.62
    
        # getting the pen position and checking if it's in the working area
        pen_pos = p.getLinkState(self.robot_id, self.penJoint)[0]
        #print("pen position: ", pen_pos)
        if pen_pos[0] < x_min or pen_pos[0] > x_max:
            if self.logs:
                print(f"Out of working area. The pen is currently out of the working area in X")
            return False
        if pen_pos[1] < y_min or pen_pos[1] > y_max:
            if self.logs:
                print(f"Out of working area. The pen is currently out of the working area in Y")
            return False
        if pen_pos[2] < z_min or pen_pos[2] > z_max:
            if self.logs:
                print(f"Out of working area. The pen is currently out of the working area in Z")
            return False
        # If the pen is within the working area, return True
        return True

    def checkingCollision(self, angles):
        threshold_distance = 0.005 # 5mm safety margin
        contact_points_robot = p.getContactPoints(self.robot_id, self.robot_id)  
        contact_points_ground = p.getContactPoints(self.robot_id, self.ground_id)  

        # Check for potential self-collisions within 5mm
        # close_contacts_robot = p.getClosestPoints(self.robot_id, self.robot_id, distance=threshold_distance)
        # close_contacts_ground = p.getClosestPoints(self.robot_id, self.ground_id, distance=threshold_distance)

        isInCollision = True
        if self.logs:
            print(f"Checking collision for angles: {angles}")

        def getLinkName(id):
            return (p.getJointInfo(self.robot_id, id)[12]).decode()

        # #Check self-collisions (ignoring wrist-pen collision)
        for contact in contact_points_robot:
            if getLinkName(contact[3]) == "wrist_3_link" and getLinkName(contact[4]) == "pen_link":
                continue
            if self.logs:
                print(f"Self-Collision: {getLinkName(contact[3])} and {getLinkName(contact[4])} are colliding.")
            isInCollision = False

        # Check ground collisions
        for contact in contact_points_ground:
            if getLinkName(contact[3]) == "base_link_inertia":
                continue
            if self.logs:
                print(f"Collision with Ground: {getLinkName(contact[3])} touched the ground!")
            isInCollision = False

        # Check if a collision is **about to happen** within 5mm
        # for contact in close_contacts_robot:
        #     if (contact[3] == contact[4] or 
        #         abs(contact[3] - contact[4]) == 1 or 
        #         getLinkName(contact[3]) == "pen_link" or 
        #         getLinkName(contact[4]) == "pen_link"):  # Exclude collisions between the same link, adjacent links, or involving the pen link
        #         continue
        #     if self.logs:
        #         print(f"WARNING: {getLinkName(contact[3])} is too close to {getLinkName(contact[4])} (within {threshold_distance})!")
        #     isInCollision = False  # Prevent movement if too close

        # for contact in close_contacts_ground:
        #     if getLinkName(contact[3]) == "base_link_inertia":
        #         continue
        #     if self.logs:
        #         print(f"WARNING: {getLinkName(contact[3])} is too close to the ground (within 5mm)!")
        #     isInCollision = False  # Prevent movement if too close

        if not self.check_working_area():
            isInCollision = False

        if self.logs:
            print("\n")

        return isInCollision

    

    
    def isValidConfiguration(self,angles):
           # Set the robot to the desired joint configuration
        for i, joint_id in enumerate(self.mapping.values()):
            p.resetJointState(self.robot_id, joint_id, angles[i])
        p.stepSimulation()

        return self.checkingCollision(angles)  # True if no collisions, False otherwise
        
    def runSimulation(self, angles):

        collison = False 
        collison = self.isValidConfiguration(angles)
        while p.isConnected():
            if collison !=  None:
                if self.gui:
                    time.sleep(2)                    
                return collison

    
 
collison = [ 0.0, -3.14, 2.2, 0.6, 3.0, 0.0]
nocoll = [0.9509, -1.6623, 0.6353, -0.5976, -1.5722, 0.0]
collGround = [ 1.5,-3.9,-3, 0.0, 0.0, 0.0]
testAngles =   [
                -0.1122,
                -3.0658,
                0.4916,
                2.5814,
                1.4586,
                -1.5638
            ]
if __name__ == "__main__":
   
    # iscoin = ISCoin(host="10.30.5.159", opened_gripper_size_mm=40)
    # angles= list(iscoin.robot_control.get_actual_joint_positions())
    # print(angles)
    test = RobotCollisionCheck ()
    print("coll res",test.runSimulation(nocoll)
    )
    print("working area", test.check_working_area())