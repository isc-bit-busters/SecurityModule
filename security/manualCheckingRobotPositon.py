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

            self._validate(self.robotPosition[0])
            self.line = []
            for i in range(1,len(self.robotPosition)):
                self._validate(self.robotPosition[i])
        
            self.finalPositions.append(self.line)



    def _validate(self, angles: list[float]):
        checkingTasks = GlobalRobotChecking(angles, self.logs)
        angle = checkingTasks.checkNextBehaviour()  
    #if len(angle) != 0:
        self.line.append([list(map(float, x)) for x in angle])


