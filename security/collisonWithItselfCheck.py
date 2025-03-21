import numpy as np

from .forwardKinematics import ForwardKinematic
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import matplotlib.pyplot as plt
import plotly.graph_objects as go

class RobotCollisonWithItselfChecking:
    def __init__(self, angles: list[float]):
        self.angles = angles
        self.diameters = {
            1: 0.128,  # to be defined
            2: 0.09,
            3: 0.09,
            4: 0.065,
            5: 0.065,
            6: 0.065,
        }
        self.safeDistances = {
            1: {2: 0.07, 3: 0.05, 4: 0.05, 5: 0.08, 6: 0.3},
            2: {3: 0.01, 4: 0.001, 5: 0.01, 6: 0.01},
            3: {4: 0.01, 5: 0.01, 6: 0.01},
            4: {5: 0.01, 6: 0.01},
            5: {6: 0.01},
        }
        self.cylinders = {}

        self.coordinates = ForwardKinematic(angles).getCoordinates()
        self._fillCylindersDict()


    def _createVectorCylinder(self, p1, q1):
        """Creation of a vector from two points
        to define the direction of the cylinder"""
        print("vector d ", np.array([(q1["x"] - p1["x"]), (q1["y"] - p1["y"]), (q1["z"] - p1["z"])]))
        print("distance: ", np.linalg.norm(np.array([(q1["x"] - p1["x"]), (q1["y"] - p1["y"]), (q1["z"] - p1["z"])])))
        return np.array([(q1["x"] - p1["x"]), (q1["y"] - p1["y"]), (q1["z"] - p1["z"])])
    def _createCylinder(self, key, p1, q1):
        """Create a cylinder with the given coordinates and radius"""

        if key == 6:
            # Extend the cylinder with key 6 by scaling its direction vector
            extension_factor = 1.5  # Adjust this factor to control the length
            direction_vector = self._createVectorCylinder(p1, q1)
            extended_q1 = {
                "x": q1["x"] + extension_factor * direction_vector[0],
                "y": q1["y"] + extension_factor * direction_vector[1],
                "z": q1["z"] + extension_factor * direction_vector[2],
            }
            self.cylinders[key] = {
                "p": p1,
                "q": q1,
                "r": self.diameters[key] / 2,
                "d": direction_vector,
            }
        else:
            self.cylinders[key] = {
                "p": p1,
                "q": q1,
                "r": self.diameters[key] / 2,
                "d": self._createVectorCylinder(p1, q1),
            }

    def _fillCylindersDict(self):
        for key, value in self.coordinates.items():
            if key < 6:
                self._createCylinder(key, value, self.coordinates[key + 1])
            else:
                break

    def _closest_points_between_segments(self, p1, q1, p2, q2):
        """Find the closest points between two line segments."""
        # Convert points to numpy arrays
        p1 = np.array([p1["x"], p1["y"], p1["z"]])
        q1 = np.array([q1["x"], q1["y"], q1["z"]])
        p2 = np.array([p2["x"], p2["y"], p2["z"]])
        q2 = np.array([q2["x"], q2["y"], q2["z"]])

        # Direction vectors of the segments
        d1 = q1 - p1
        d2 = q2 - p2
        r = p1 - p2

        # Compute parameters for the closest points
        a = np.dot(d1, d1)
        b = np.dot(d1, d2)
        c = np.dot(d2, d2)
        d = np.dot(d1, r)
        e = np.dot(d2, r)
        denom = a * c - b * b

        if abs(denom) < 1e-6:  # Segments are parallel
            s = 0.0
            t = e / c if c > 1e6 else 0.0
        else:
            s = (b * e - c * d) / denom
            t = (a * e - b * d) / denom

        # Clamp s and t to [0, 1] to ensure they lie within the segments
        s = max(0, min(s, 1))
        t = max(0, min(t, 1))

        # Compute closest points
        closest_p1 = p1 + s * d1
        closest_p2 = p2 + t * d2

        return closest_p1, closest_p2

    def _computeDistanceBetweenTwoAxis(self, cylinderKey1, cylinderKey2):
        """Compute the distance between two cylinders"""
        # Get the start and end points of the cylinders
        p1 = self.cylinders[cylinderKey1]["p"]
        q1 = self.cylinders[cylinderKey1]["q"]
        p2 = self.cylinders[cylinderKey2]["p"]
        q2 = self.cylinders[cylinderKey2]["q"]

        # Find the closest points between the two cylinders
        p1_array, p2_array = self._closest_points_between_segments(p1, q1, p2, q2)
        p2MinusP1 = p2_array - p1_array
        crossProd = np.cross(
            self.cylinders[cylinderKey1]["d"], self.cylinders[cylinderKey2]["d"]
        )
        crossProdNorm = np.linalg.norm(crossProd)

        if crossProdNorm == 0:
            print(f"Warning: Cylinders {cylinderKey1} and {cylinderKey2} are parallel.")
            return np.linalg.norm(p2MinusP1)  # Use a fallback distance

        dotProd = np.dot(p2MinusP1, crossProd)
        distance = abs(dotProd / crossProdNorm)

        print(f"Distance axes between {cylinderKey1} and {cylinderKey2}: {distance}")
        return distance

    def _computeDistanceBetweenTwoCylinders(self, cylinderKey1, cylinderKey2):
        """Compute the distance between two cylinders"""
        dAxes = self._computeDistanceBetweenTwoAxis(cylinderKey1, cylinderKey2)

        r1 = self.cylinders[cylinderKey1]["r"] / 2
        r2 = self.cylinders[cylinderKey2]["r"] / 2

        print(f"Radii: Cylinder {cylinderKey1} = {r1}, Cylinder {cylinderKey2} = {r2}")

        return dAxes - (r1 + r2)

    def checkingCollisonWithItself(self):
        cylinderDistances = {}

        cylinder_keys = list(self.cylinders.keys())  # Extract just the keys

        for i, key1 in enumerate(cylinder_keys):
            for key2 in cylinder_keys[i + 1 :]:  # Ensure unique comparisons
                if key2 == key1 + 1:  # Skip consecutive cylinders
                    continue

                if key2 in self.safeDistances.get(key1, {}):  # Avoid KeyError
                    distance = self._computeDistanceBetweenTwoCylinders(key1, key2)
                    print("distance", key1, key2, distance)

                    if distance < self.safeDistances[key1][key2]:
                        cylinderDistances[(key1, key2)] = False
                    else:
                        cylinderDistances[(key1, key2)] = True
        return cylinderDistances

    def plotCylinders(self):
        """Plot the cylinders in 3D space interactively using plotly."""
        
        fig = go.Figure()

        for key, cylinder in self.cylinders.items():
            p = np.array([cylinder["p"]["x"], cylinder["p"]["y"], cylinder["p"]["z"]])
            q = np.array([cylinder["q"]["x"], cylinder["q"]["y"], cylinder["q"]["z"]])
            r = cylinder["r"]

            # Plot the cylinder axis as a line
            fig.add_trace(go.Scatter3d(
                x=[p[0], q[0]],
                y=[p[1], q[1]],
                z=[p[2], q[2]],
                mode='lines',
                line=dict(width=r*1000),
                name=f"Cylinder {key}"
            ))

            # Generate the circular cross-sections along the cylinder's height
            v = np.linspace(0, 2 * np.pi, 100)
            x_circle = r * np.cos(v)
            y_circle = r * np.sin(v)

            # Create the cylinder by plotting multiple cross-sections
            for t in np.linspace(0, 1, 10):
                point = p + t * (q - p)
                fig.add_trace(go.Scatter3d(
                    x=x_circle + point[0],
                    y=y_circle + point[1],
                    z=np.full_like(x_circle, point[2]),
                    mode='lines',
                    line=dict(color='rgba(0,0,255,0.3)', width=2),
                    showlegend=False
                ))

        # Labels and visualization settings
        fig.update_layout(
            scene=dict(
                xaxis_title="X-axis",
                yaxis_title="Y-axis",
                zaxis_title="Z-axis"
            ),
            title="3D Cylinder Visualization",
        )
        
        fig.show()




# Test angles
collisionAngle1 = [0.9509, -1.6623, 2.3, -0.5976, 0.5, 0.0] # ok
safeAngle1 = [0.9509, -1.6623, 0.6353, -0.5976, -1.5722, 0.0] # ok
safeAngle2 = [0.9509, -1.6623, 0.6353, -0.5976, -1.5722, 0.0]
collisionAngle2 = [0.9509, -1.6623, -3.0, 0.5976, 0.5722, 0.0]
collisionAngle3 = [0.00001, -3.13, 3.13, 0.000001, 0.000001, 0.000001]
collisionAngle4 = [0.00001, 0.000001, 0.000001, 0.000001, 0.000001, 0.000001]
collisionAngle5 = [0.0001, -3.14, 2.7, 0.0001, 3.14, 0.0001]
collisionAngle6 = [0.00001, -3.14, 3.14, 0.00001, 3.14, 0.000001]
collisionAngle7 = [0.9509, -1.6623, 0.6353, 0.5, -1.5722, 0.0]
noColl = [0.9019, -1.1795, 1.9326, -2.3253, -1.5697, -0.6689]
safeAngle3 = [-0.7493, -1.0, 1.0478, -1.0997, -0.2, -2.3201]
safeAngle4 = [0.7493, -1.5177, 1.0478, -1.0997, -1.5695, -2.3201]
if __name__ == "__main__":
    test1 = RobotCollisonWithItselfChecking(collisionAngle7)

    print(test1.checkingCollisonWithItself())
    test1.plotCylinders()
   # test2.plotCylinders()
