import math


class RobotPositonChecking(): 

    def __init__(self):
        # make a struct to stock min distance btw 2 joints
        pass


    def _computeDistanceBtwTwoJoints(self,j1, j2):
        return math.sqrt((j2["x"] - j1["x"])**2 + (j2["y"] - j1["y"])**2 + (j2["z"] - j1["z"])**2)
        


    def checkingDistanceFromGround(): 

        pass

        
#TODO : check that angles have correct values compare those from before with sctual ones