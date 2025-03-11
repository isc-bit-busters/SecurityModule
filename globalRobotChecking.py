import threading
import time
from checkAnglesVariation import checkAngleVariation
from robotPositionChecking import RobotPositonChecking
from workingAreaChecking import WorkingAreaRobotChecking
from urbasic.URBasic import ISCoin

class GlobalRobotChecking():
    def __init__(self, angles: list,interval:float = None, holdAngles = None,iscoin = None):

        self.interval = interval
        self.running = False
        if holdAngles is None:
            self.holdAngles = angles
        else:
            self.holdAngles = holdAngles
        self.angles = angles
        self._thread = None  
        self._stop_event = threading.Event()  # Event to handle stopping
        self.deltaT = 0.01
        #self.iscoin = iscoin
        self.validPositions = []
        self.isValid = True

    def start(self):
        self.running = True  
        self._stop_event.clear()  # Ensure stop event is not set
        self._thread = threading.Thread(target=self._run_task, daemon=True)
        self._thread.start()

    def _run_task(self):
        """The actual task that will be repeated"""
        i = 0
        while not self._stop_event.is_set():  # Continue running until stop is requested
            #self.angles = self.iscoin.robot_control.get_actual_joint_positions()
            print(self.angles)
            self.angles = [i,i,i,i,i,i]
            i += 1
            self.checkNextBehaviour() 
            self.isValid = True 
            self._stop_event.wait(self.interval)  # Non-blocking sleep

    def stop(self):
        """Stop the task"""
        self._stop_event.set()  # Signal the thread to stop
        if self._thread is not None:
            self._thread.join() 
         

    # test effectued only for the real time checking
    def _beahviourForRealTime(self):
        highVariations = []
        if len(set(self.angles)) == len(self.holdAngles):
            highVariations, self.holdAngles = checkAngleVariation(self.angles, self.holdAngles, self.interval).checkVariation()

        if highVariations:
            print("High variations in the angles of the joints: ", highVariations)
            self.isValid = False 
        else: 
            print("The angles of the joints are stable")
        
    def checkNextBehaviour(self):

        if self.interval is not None:
            self._beahviourForRealTime()

        self.safeAreaChecking = WorkingAreaRobotChecking(0, 0, 0, 0.5, self.angles).checkPointsInHalfOfSphere()
        #WorkingAreaRobotChecking(0, 0, 0, 0.5, self.angles).draw()
        self.checkingDistanceFromTheGround = RobotPositonChecking(self.angles).checkingDistanceFromGround()
        if any(value is False for value in self.safeAreaChecking.values()):
            print("Robot is out of the working area")
            self.isValid = False
        else:
            print("Robot is inside the working area")

        if any(value is False for value in self.checkingDistanceFromTheGround.values()):  
            print("Robot is too close to the ground") 
            self.isValid = False
        else:
            print("Robot is at a safe distance from the ground")
     
        if  self.isValid:
            self.validPositions.append(self.angles)
            return self.validPositions

