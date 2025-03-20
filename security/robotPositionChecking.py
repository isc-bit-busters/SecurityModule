import math



from forwardKinematics import ForwardKinematic
from workingAreaChecking import WorkingAreaRobotChecking



class DistanceFromGroundChecking(): 

    def __init__(self, angles:list):
        self.angles = angles
        self.coordinates = ForwardKinematic(angles).getCoordinates()
        self.safeDistancesFromTheGround= { # ipothetic values of minimun allowed distances of each joint from the ground base excluded
            3 : 0.1, 
            4 : 0.1, 
            5 : 0.1,
            6: 0.2
        }



    def _computeDistanceBtwTwoJoints(self,j1, j2):
        return math.sqrt((j2["x"] - j1["x"])**2 + (j2["y"] - j1["y"])**2 + (j2["z"] - j1["z"])**2)
        

    # Compute distance of each joint from the ground with a trigo approach 
    def _computeDistanceFromGround(self, joint_index):
    
        j1 = self.coordinates[1]  # Base joint (reference)
        j2 = self.coordinates[joint_index]  # Target joint

        distanceBtwTwoJoint = self._computeDistanceBtwTwoJoints(j1, j2)

        alphaAngle = self.angles[0]  # Assuming Joint 2 corresponds to index 1
        betaAngle = self.angles[joint_index]

        gammaAngle = math.pi - (alphaAngle + betaAngle)
        return abs(distanceBtwTwoJoint * (math.sin(math.radians(alphaAngle)) / math.sin(math.radians(gammaAngle))))



    def checkingDistanceFromGround(self):

        checkingDistance = {}
        distancesFromTheGround= {
            i+1 :{ self._computeDistanceFromGround(i)
                  
            } for i in range(2,len(self.coordinates)) # base exluded
        } 
        for (keyReal, dReal), (keyMin, dMin) in zip(distancesFromTheGround.items(), self.safeDistancesFromTheGround.items()):
            print(keyReal,dReal)
            if float(next(iter(dReal))) <= dMin :
                checkingDistance[keyReal] = False
            else :
                checkingDistance[keyReal] = True
        
        return checkingDistance

angleTest1 =[
                0.9509,
                -1.6623,
                0.6353,
                -0.5976,
                -1.5722,
                0.0
            ]
angleTest2 = [
                0.9019,
                -0.28,
                1.7852,
                -3.0774,
                -1.5697,
                -0.6689
            ]
workingAreaRobotChecking = WorkingAreaRobotChecking(0, 0, 0, 0.7, angleTest1)
workingAreaRobotChecking.draw()
print(workingAreaRobotChecking.checkPointsInHalfOfSphere())

test = DistanceFromGroundChecking(angleTest1)
print(test.checkingDistanceFromGround())


