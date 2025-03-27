import numpy as np

from .globalRobotChecking import GlobalRobotChecking


class ValidateRobotPosition():
    def __init__(self, allRobotPosition: list[list[list[float]]], logs = True):
        self.logs = logs
        self.allRobotPosition = allRobotPosition
        self.finalPositions = []
        self.line= []
        for i in range(len(self.allRobotPosition)):
            self.robotPosition = self.allRobotPosition[i]

            
            self.line = []
            for i in range(0,len(self.robotPosition)):
                self._validate(self.robotPosition[i])
        
            self.finalPositions.append(self.line)



    def _validate(self, angles: list[float]):
        checkingTasks = GlobalRobotChecking(angles, self.logs)
        angle = checkingTasks.checkNextBehaviour()  
        if len(angle) != 0:
            self.line.append(angles)


