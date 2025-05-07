import numpy as np
import matplotlib.pyplot as plt

from .forwardKinematics import ForwardKinematic

class WorkingAreaRobotChecking():
    def __init__(self, x0, y0, z0, r, angles:list, unitTest = False, coordinates = None):
        """
        Initializes the WorkingAreaRobotChecking class.

        Parameters:
        - x0, y0, z0: Coordinates of the sphere's center.
        - r: Radius of the sphere.
        - angles: List of joint angles for the robot.
        - unitTest: Boolean flag to enable unit testing.
        - coordinates: Predefined coordinates for unit testing.
        """
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.r = r
        
        # Get robot joint coordinates using forward kinematics
        self.coordinates = ForwardKinematic(angles).getCoordinates()

        # Override coordinates if unit testing is enabled
        if unitTest:
            self.coordinates = coordinates

        # Generate points on the sphere's surface
        num_points = 50
        theta = np.linspace(0, 2 * np.pi, num_points)  # Azimuthal angle
        phi = np.linspace(0, np.pi, num_points)       # Polar angle

        # Create a meshgrid for spherical coordinates
        theta, phi = np.meshgrid(theta, phi)

        # Convert spherical coordinates to Cartesian coordinates
        x = self.x0 + self.r * np.cos(theta) * np.sin(phi)
        y = self.y0 + self.r * np.sin(theta) * np.sin(phi)
        z = self.z0 + self.r * np.cos(phi)

        # Flatten the arrays for easier processing
        x_flat = x.flatten()
        y_flat = y.flatten()
        z_flat = z.flatten()

        # Combine the coordinates into a single array
        points = np.vstack((x_flat, y_flat, z_flat)).T

        # Filter points to only include those in the lower hemisphere (z < 0)
        self.points_filtered = points[points[:, 2] < 0]

    def _isPointInHalfOfSphere(self, randomPoint):
        """
        Checks if a given point is within the lower hemisphere

        Parameters:
        - randomPoint: A list containing the x, y, z coordinates of the point.

        Returns:
        - True if the point is within the specified region, False otherwise.
        """
        # Check if the point is in the lower hemisphere (z < 0)
        if randomPoint[2] < 0:
            return False
        # Check if the point is within the sphere's radius
        return (randomPoint[0] - self.x0)**2 + (randomPoint[1] - self.y0)**2 + (randomPoint[2] - self.z0)**2 <= self.r**2

    def draw(self):
        """
        Visualizes the working area and the robot's joint positions in 3D space.
        """
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

        # Plot the filtered hemisphere points
        ax.scatter(x_filtered, y_filtered, z_filtered, alpha=0.5, label="Working Area")

        # Plot the robot joint positions
        ax.scatter(x_vals, y_vals, z_vals, c='red', s=10, label="Robot Joints")

        # Connect the robot joints with lines
        for i in range(len(x_vals) - 1):  # Loop through consecutive points
            ax.plot([x_vals[i], x_vals[i+1]],  # X-coordinates
                    [y_vals[i], y_vals[i+1]],  # Y-coordinates
                    [z_vals[i], z_vals[i+1]],  # Z-coordinates
                    c='blue', linewidth=2)  # Blue lines

        # Set axis labels and legend
        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")
        ax.set_zlabel("Z-axis")
        ax.set_zlim((0, 1))  # Limit the Z-axis range
        plt.show()

    def checkPointsInHalfOfSphere(self):
        """
        Checks if the latest robot joint position is within the specified region.

        Returns:
        - A dictionary with the latest joint key and a boolean indicating if it's in the region.
        - None if the coordinates dictionary is empty.
        """
        if not self.coordinates:
            return None  # Return None if no coordinates are available
        
        # Get the latest joint key and its corresponding point
        latest_key = next(reversed(self.coordinates))  # Get the last added key
        latest_point = self.coordinates[latest_key]   # Get the corresponding point
        
        # Check if the point is within the specified region
        return {latest_key: self._isPointInHalfOfSphere([latest_point['x'], latest_point['y'], latest_point['z']])}