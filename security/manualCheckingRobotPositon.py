import numpy as np

from .globalRobotChecking import GlobalRobotChecking


class ValidateRobotPosition():
    def __init__(self, allRobotPosition: list[list[list[float]]]):
        self.allRobotPosition = allRobotPosition
        self.finalPositions = []
        self.line= []
        for i in range(len(self.allRobotPosition)):
            self.robotPosition = self.allRobotPosition[i]

            self._validate(self.robotPosition[0], None)
            self.line = []
            for i in range(1,len(self.robotPosition)):
                self._validate(self.robotPosition[i], self.robotPosition[i-1])
            self.finalPositions.append(self.line)



    def _validate(self, angles: list[float], holdAngles :list[float]):
        checkingTasks = GlobalRobotChecking(angles)
        self.line.append(checkingTasks.checkNextBehaviour())

