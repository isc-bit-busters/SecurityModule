
from .forwardKinematics import ForwardKinematic


class DistanceFromGroundChecking:
    def __init__(self, angles: list):
        self.angles = angles
        self.coordinates = ForwardKinematic(angles).getCoordinates()
        self.safeDistancesFromTheGround = 0.01 # safe distance from the ground
        self.wirstLength = 0.03# length of the wirst to add on z axis

        self._addWirst()
    
    def _addWirst(self):
        
        self.coordinates[6]["z"] = self.coordinates[6]["z"] - self.wirstLength

    def checkDistanceFromTheGround(self):
        result = {}
        for joint_index in range(1, 7):  # Assuming there are 6 joints
            coord = self.coordinates.get(joint_index)
            print(coord)
            print(coord["z"]+ self.safeDistancesFromTheGround)
            result[joint_index] = coord["z"] + self.safeDistancesFromTheGround >= 0.0 
        return result

