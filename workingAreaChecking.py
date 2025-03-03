import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class Sphere():
    def __init__(self, x0, y0, z0, r):
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.r = r
                
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

        # Only select points where z > 0
        self.points_filtered = points[points[:, 2] > 0]
        self.points_filtered = points[points[:, 1] > 0]

    def isPointInHalfOfSphere(self, randomPoint):
        # Check if the point is in the upper hemisphere
        if randomPoint[2] < 0:
            return False
            
        if randomPoint[1] < 0:
            return False

        # Check if the point is within the sphere's radius
        return (randomPoint[0] - self.x0)**2 + (randomPoint[1] - self.y0)**2 + (randomPoint[2] - self.z0)**2 <= self.r**2

    def draw(self, randomPoint):
        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111, projection='3d')

        # Extract X, Y, Z from generated points
        x_vals, y_vals, z_vals = self.points_filtered[:, 0], self.points_filtered[:, 1], self.points_filtered[:, 2]

        ax.scatter(x_vals, y_vals, z_vals, s=10)  # Small dots for better visualization
        ax.scatter(randomPoint[0], randomPoint[1], randomPoint[2], color='r', s=100)  # Red dot for the point
        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")
        ax.set_zlabel("Z-axis")
        plt.show()
        
        
    def areInHalfOfSphere(self, randomPoints):
        return [self.isPointInHalfOfSphere(point) for point in randomPoints]
    
    def areAllInHalfOfSphere(self, randomPoints):
        return all(self.areInHalfOfSphere(randomPoints))


# Create an instance of Sphere with center (0, 0, 0) and radius 500
sphere = Sphere(0, 0, 0, 500)

# Random point to check
random_point = (480, 4, 20)

# Draw the sphere and the random point
sphere.draw(random_point)

# Check if the random point is inside the sphere
print(sphere.isPointInHalfOfSphere(random_point))
