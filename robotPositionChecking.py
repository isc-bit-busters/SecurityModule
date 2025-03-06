import math

from forwardKinematics.forwardKInematics import ForwardKinematics


class RobotPositonChecking(): 

    def __init__(self, angles:list):
        self.coordinates = ForwardKinematics(angles).getCoordinates()
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
    def _computeDistanceFromGround(self, j):

        j1 = self.coordinates[2] # base excluded
        j2 = j

        distanceBtwTwoJoint = self._computeDistanceBtwTwoJoints(j1,j2)
        alphaAngle = int(list(j1)[0])
        betaAngle =  int(list(j2)[0])
        gammaAngle = 180 -(alphaAngle + betaAngle)

        return distanceBtwTwoJoint * (math.sin(alphaAngle)/math.sin(gammaAngle))
    


    def checkingDistanceFromGround(self):

        checkingDistance = {}
        distancesFromTheGround= {
            i+1 :{ self._computeDistanceFromGround(i)
                  
            } for i in range(1,len(self.coordinates)) # base exluded
        } 

        for (keyReal, dReal), (keyMin, dMin) in zip(distancesFromTheGround.items(), self.safeDistancesFromTheGround.items()):
            if dReal <= dMin :
                checkingDistance[keyReal] = False
            else :
                checkingDistance[keyReal] = True

        return checkingDistance
  
