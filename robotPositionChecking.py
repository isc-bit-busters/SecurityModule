import math



from forwardKinematics import ForwardKinematic



class RobotPositonChecking(): 

    def __init__(self, angles:list):
        self.angles = angles
        self.coordinates = ForwardKinematic(angles).getCoordinates()
        self.safeDistancesFromTheGround= { # ipothetic values of minimun allowed distances of each joint from the ground base excluded
            2 : 3,
            3 : 5, 
            4 : 4, 
            5 : 7,
            6 : 8
        }

        # store min distance btw 2 joints
        


    def _computeDistanceBtwTwoJoints(self,j1, j2):
        return math.sqrt((j2["x"] - j1["x"])**2 + (j2["y"] - j1["y"])**2 + (j2["z"] - j1["z"])**2)
        

    # Compute distance of each joint from the ground with a trigo approach 
    def _computeDistanceFromGround(self, joint_index):
    
        j1 = self.coordinates[1]  # Base joint (reference)
        j2 = self.coordinates[joint_index]  # Target joint

        distanceBtwTwoJoint = self._computeDistanceBtwTwoJoints(j1, j2)

        alphaAngle = self.angles[1]  # Assuming Joint 2 corresponds to index 1
        betaAngle = self.angles[joint_index]

        gammaAngle = math.pi - (alphaAngle + betaAngle)

        return distanceBtwTwoJoint * (math.sin(math.radians(alphaAngle)) / math.sin(math.radians(gammaAngle)))



    def checkingDistanceFromGround(self):

        checkingDistance = {}
        distancesFromTheGround= {
            i+1 :{ self._computeDistanceFromGround(i)
                  
            } for i in range(3,len(self.coordinates)) # base exluded
        } 

        for (keyReal, dReal), (keyMin, dMin) in zip(distancesFromTheGround.items(), self.safeDistancesFromTheGround.items()):
            if float(next(iter(dReal))) <= dMin :
                checkingDistance[keyReal] = False
            else :
                checkingDistance[keyReal] = True

        return checkingDistance
  


if __name__ == "__main__":
    test = RobotPositonChecking([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    print(test.checkingDistanceFromGround())
