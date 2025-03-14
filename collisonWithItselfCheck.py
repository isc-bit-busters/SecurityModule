import numpy as np

from forwardKinematics import ForwardKinematic


class RobotCollisonWithItselfChecking:
    def __init__(self, angles: list[float]):
        self.angles = angles
        self.diameters = {
            1: 0.128,  # to be defined
            2: 0.128,
            3: 0.05,
            4: 0.05,
            5: 0.01,
            6: 0.01,
        }
        self.safeDistances = {
            1: {2: 0.01, 3: 0.03, 4: 0.01, 5: 0.01, 6: 0.01},
            2: {3: 0.01, 4: 0.01, 5: 0.001, 6: 0.01},
            3: {4: 0.01, 5: 0.01, 6: 0.01},
            4: {5: 0.01, 6: 0.01},
            5: {6: 0.01},
        }
        self.cylinders = {}

        self.coordinates = ForwardKinematic(angles).getCoordinates()
    

    def _createVectorCylinder(self, p1, q1):
        """Creation of a vector from two points
        to define the direction of the cylinder"""
        return [(q1["x"] - p1["x"]), (q1["y"] - p1["y"]), (q1["z"] - p1["z"])]

    def _createCylinder(self, key, p1, q1):
        """Create a cylinder with the given coordinates and radius"""
        self.cylinders[key] = {
            "p": p1,
            "q": q1,
            "r": self.diameters[key],
            "d": self._createVectorCylinder(p1, q1),
        }

    def _fillCylindersDict(self):
        for key, value in self.coordinates.items():
            if key < 6:
                self._createCylinder(key, value, self.coordinates[key + 1])
            else:
                break

    def _computeDistanceBetweenTwoAxis(self, cylinderKey1, cylinderKey2):
        """Compute the distance between two axis/ lines"""

        p1 = self.cylinders[cylinderKey1]["p"]
        p2 = self.cylinders[cylinderKey2]["p"]
        p1_array = np.array([p1["x"], p1["y"], p1["z"]])
        p2_array = np.array([p2["x"], p2["y"], p2["z"]])

        p2MinusP1 = p2_array - p1_array
        crossProd = np.cross(
            self.cylinders[cylinderKey1]["d"], self.cylinders[cylinderKey2]["d"]
        )
        crossProdNorm = np.linalg.norm(crossProd)
        dotProd = np.dot(p2MinusP1, crossProd)
        return abs(dotProd / crossProdNorm)

    def _computeDistanceBetweenTwoCylinders(self, cylinderKey1, cylinderKey2):
        """Compute the distance between two cylinders"""

        dAxes = self._computeDistanceBetweenTwoAxis(cylinderKey1, cylinderKey2)
        r1 = self.cylinders[cylinderKey1]["r"]
        r2 = self.cylinders[cylinderKey2]["r"]
        return dAxes - (r1 + r2)

    def checkingCollisonWithItself(self):
        self._fillCylindersDict()
        cylinderDistances = {}

        cylinder_keys = list(self.cylinders.keys())  # Extract just the keys
        
        for i, key1 in enumerate(cylinder_keys):  
            for key2 in cylinder_keys[i+1:]:  # Ensure unique comparisons
                if key2 in self.safeDistances.get(key1, {}):  # Avoid KeyError

                    distance = self._computeDistanceBetweenTwoCylinders(key1, key2)
                    print(key1, key2,distance)

                    if abs(distance) < self.safeDistances[key1][key2]:
                        cylinderDistances[(key1, key2)] = False
                    else:
                        cylinderDistances[(key1, key2)] = True

        return cylinderDistances


    #

collisionAngle1 = [
                0.9509,
                -1.6623,
                1.8353,
                -0.5976,
                -1.5722,
                0.0
            ]
safeAngle1 =  [
               
                0.9509,
                -1.6623,
                0.6353,
                -0.5976,
                -1.5722,
                0.0
            ]
safeAngle2 = [
                0.9509,
                -1.6623,
                0.6353,
                -0.5976,
                -1.5722,
                0.0
            ]
collisionAngle2= [
                0.9509,
                -1.6623,
                2.6353,
                0.5976,
                1.5722,
                0.0
            ]

if __name__ == "__main__":
    test1 = RobotCollisonWithItselfChecking( collisionAngle2 )
    test2 = RobotCollisonWithItselfChecking( safeAngle2 )

print(test1.checkingCollisonWithItself())
print(test2.checkingCollisonWithItself())