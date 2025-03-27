import threading

from urbasic import ISCoin
import numpy as np

from .checkAnglesVariation import checkAngleVariation
from .workingAreaChecking import WorkingAreaRobotChecking
from .collisionChecking import RobotCollisionWithItselfChecking

class GlobalRobotChecking():
    def __init__(self, angles: list[float], logs=True,  interval: float = None, iscoin: ISCoin = None):
        """
        Initializes the GlobalRobotChecking class.

        Parameters:
        - angles: List of initial joint angles for the robot.
        - interval: Time interval for real-time checking.
        - iscoin: Instance of ISCoin for robot control.
        """
        self.interval = interval  # Time interval for periodic checks
        self.running = False  # Flag to indicate if the checking is running
        self.holdAngles = angles  # Store the initial angles
        self.angles = angles  # Current joint angles
        self._thread = None  # Thread for running the task
        self._stop_event = threading.Event()  # Event to handle stopping the thread
        self.deltaT = interval  # Time interval for checks
        self.iscoin = iscoin  # Robot control instance
        self.validPositions = []  # List to store valid positions
        self.isValid = True  # Flag to indicate if the robot is in a valid state
        self.logs = logs  # Flag to indicate if logs should be printed

    def start(self):
        """
        Starts the real-time checking process in a separate thread.
        """
        self.running = True  # Set the running flag to True
        self._stop_event.clear()  # Clear the stop event
        self._thread = threading.Thread(target=self._run_task, daemon=True)  # Create a daemon thread
        self._thread.start()  # Start the thread

    def _run_task(self):
        """
        The task that runs periodically to check the robot's behavior.
        """
        while True:  # Continue running until stop is requested
            # Get the current joint positions from the robot
            self.angles = self.iscoin.robot_control.get_actual_joint_positions().toList()
            self.validPositions = []
            self.validPositions=self.checkNextBehaviour()  # Perform the next behavior check
            if not self.validPositions: 
                self.iscoin.robot_control.stopj(self.angles)
                break
            self._stop_event.wait(self.interval)  # Wait for the specified interval (non-blocking sleep)
    



    def stop(self):
        """
        Stops the real-time checking process.
        """
        self._stop_event.set()  # Signal the thread to stop
        if self._thread is not None:
            self._thread.join()  # Wait for the thread to finish

    def _beahviourForRealTime(self):
        """
        Checks for high variations in joint angles during real-time operation.
        """
        highVariations = []  # List to store joints with high variations

        # Check for angle variations and update holdAngles
        highVariations, self.holdAngles = checkAngleVariation(self.angles, self.holdAngles, self.interval).checkVariation()
        self.holdAngles = self.angles  # Update holdAngles with the current angles

        # If high variations are detected, print a warning and mark the state as invalid
        if highVariations and self.logs:
            print("High variations in the angles of the joints: ", highVariations)
            self.isValid = False

    def checkNextBehaviour(self):
        """
        Performs various checks to ensure the robot is operating within safe parameters.
        """

        if self.logs:
            print("===== Checking pose =====")

        isCurrentAngleValid = True

        # Perform real-time behavior checks if an interval is specified
        if self.interval is not None:
            self._beahviourForRealTime()
        # Check if the robot is within the working area
        self.safeAreaChecking = WorkingAreaRobotChecking(0, 0, 0, 0.62, self.angles)
        areaChecking = self.safeAreaChecking.checkPointsInHalfOfSphere()

        # Check if the robot is too close to the ground
        self.checkingDistanceFromTheGround = RobotCollisionWithItselfChecking(self.angles).checkingCollisionWithGround()

        # Check if the robot is colliding with itself
        self.checkDistFromItself = RobotCollisionWithItselfChecking(self.angles).checkingCollisionWithItself()

        # If the robot is out of the working area, print a warning and mark the state as invalid
        if areaChecking[6] != np.True_:
            if self.logs:
                print("Robot is out of the working area")
            isCurrentAngleValid = False

        # If the robot is too close to the ground, print a warning and mark the state as invalid
        if any(value is np.False_ for value in self.checkingDistanceFromTheGround.values()):
            if self.logs:
                print("Robot is too close to the ground")
            isCurrentAngleValid = False

        # If the robot is too close to itself, print a warning and mark the state as invalid
        if any(value is False for value in self.checkDistFromItself.values()):
            if self.logs:
                print("Robot is too close to itself")
            isCurrentAngleValid = False


        if isCurrentAngleValid:
            self.validPositions.append(self.angles)  # Append the current angles to the valid positions list

        return list(self.validPositions)
