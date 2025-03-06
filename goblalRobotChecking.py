
from robotPositionChecking import RobotPositonChecking
from workingAreaTest.workingAreaChecking import WorkingAreaRobotChecking


class GlobalRobotChecking():

    def __init__(self, angles:list):
        self.angles = angles
        self.safeAreaChecking = WorkingAreaRobotChecking(0,0,0,450).areAllInHalfOfSphere()
        self.checkingDistanceFronTheGround = RobotPositonChecking(self.angles).checkingDistanceFromGround()



    

     # maybe do this method in pricipal class 
    def establishNextBehaviour(self) :
        checkingDistance = self._checkingDistanceFromGround()
        if any(value == False for value in checkingDistance.values()): # Other conditiotion to add 
            print("Kinematics is wrong, do it again or put the robot back in its initial position ")
        else:
            print("All values are True. The kinematics works. Mouvement approuved")

        