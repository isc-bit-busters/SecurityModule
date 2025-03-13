import numpy as np

from forwardKinematics import ForwardKinematic


class RobotCollisonWithItselfChecking:
    def __init__(self, angles: list[float]):
        self.angles = angles
        self.diameters = {
            1: 0.128,  # to be defined
            2: 0.128,
            3: 0.128,
            4: 0.128,
            5: 0.128,
            6: 0.128,
        }
        self.safeDistances = {
            0: {1: 0.1, 2: 0.1, 3: 0.01, 4: 0.01, 5: 0.01},
            1: {2: 0.1, 3: 0.1, 4: 0.01, 5: 0.01},
            2: {3: 0.1, 4: 0.1, 5: 0.01},
            3: {4: 0.1, 5: 0.1},
            4: {5: 0.1},
        }
        self.cylinders = {}

        self.coordinates = ForwardKinematic(angles).getCoordinates()
        print("all cord", self.coordinates)
        print()

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
        print("cylinders", self.cylinders)

    def _computeDistanceBetweenTwoAxis(self, cylinderKey1, cylinderKey2):
        """Compute the distance between two axis/ lines"""

        print(self.cylinders[cylinderKey1]["p"])
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

        for key1, value1 in self.cylinders.items():
            items_list = list(self.cylinders.items())  # Convert dict_items to a list
            for key2, value2 in items_list[key1:]:  # Now slicing works
                if key1 != key2:
                    print(key1, key2)
                    distance = self._computeDistanceBetweenTwoCylinders(key1, key2)
                    print("here", self.safeDistances[key1][key2], "key", key1, key2)
                    if distance < self.safeDistances[key1][key2]:
                        cylinderDistances[key1] = False
                    else:
                        cylinderDistances[key1] = True

        return cylinderDistances

    #


if __name__ == "__main__":
    test = RobotCollisonWithItselfChecking(
        [
            0.9481282830238342,
            -1.3380088073066254,
            0.7121437231646937,
            -1.0540800851634522,
            -1.5575674215899866,
            -0.5976246039019983,
        ]
    )

print(test.checkingCollisonWithItself())