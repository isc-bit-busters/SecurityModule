import numpy as np
import matplotlib.pyplot as plt

from forwardKinematics import ForwardKinematic

class WorkingAreaRobotChecking():
    def __init__(self, x0, y0, z0, r, angles:list, unitTest = False, coordinates = None):

        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.r = r
        
        self.coordinates = ForwardKinematic(angles).getCoordinates()

        if unitTest:
            self.coordinates = coordinates

        num_points = 50
        theta = np.linspace(0, 2 * np.pi, num_points)  # Azimuthal angle
        phi = np.linspace(0, np.pi, num_points)      # Polar angle

        theta, phi = np.meshgrid(theta, phi)

        x = self.x0 + self.r * np.cos(theta) * np.sin(phi)
        y = self.y0 + self.r * np.sin(theta) * np.sin(phi)
        z = self.z0 + self.r * np.cos(phi)

        # Flatten the arrays
        x_flat = x.flatten()
        y_flat = y.flatten()
        z_flat = z.flatten()

        # Filter points where z > 0 (for the top hemisphere)
        points = np.vstack((x_flat, y_flat, z_flat)).T

        # Only select points where z < 0
        self.points_filtered = points[points[:, 2] < 0]
        self.points_filtered = points[points[:, 1] < 0]



    def _isPointInHalfOfSphere(self, randomPoint):
        # Check if the point is in the upper hemisphere
        if randomPoint[2] < 0:
            return False
        if randomPoint[1] < 0:
            return False
            
        # Check if the point is within the sphere's radius
        return (randomPoint[0] - self.x0)**2 + (randomPoint[1] - self.y0)**2 + (randomPoint[2] - self.z0)**2 <= self.r**2

    def draw(self):
        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111, projection='3d')

        # Extract X, Y, Z from the filtered hemisphere points
        x_filtered = self.points_filtered[:, 0]
        y_filtered = self.points_filtered[:, 1]
        z_filtered = self.points_filtered[:, 2]

        # Convert robot joint coordinates to NumPy arrays
        x_vals = np.array([point['x'] for point in self.coordinates.values()])
        y_vals = np.array([point['y'] for point in self.coordinates.values()])
        z_vals = np.array([point['z'] for point in self.coordinates.values()])

        # Plot hemisphere points
        ax.scatter(x_filtered, y_filtered, z_filtered, alpha=0.5, label="Working Area")

        # Plot robot joint positions with color and size adjustments
        ax.scatter(x_vals, y_vals, z_vals, c='red', s=10, label="Robot Joints")

    

        # Labels and legend
        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")
        ax.set_zlabel("Z-axis")

        plt.show()


    def checkPointsInHalfOfSphere(self):

        # Check if each point in the random_points dictionary is inside the upper hemisphere
        return {key: self._isPointInHalfOfSphere([point['x'], point['y'], point['z']]) 
                for key, point in self.coordinates.items()}



if __name__ == "__main__": 
    test = WorkingAreaRobotChecking(0, 0, 0, 0.5, [  0.9509,
                -1.6623,
                0.6353,
                -0.5976,
                -1.5722,
                0.0], False ) # Inside)
    print(test.checkPointsInHalfOfSphere()) 
    test.draw()