import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class WorkingAreaRobotChecking():
    def __init__(self, x0, y0, z0, r, coordinates):
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.r = r
        
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

        # Only select points where z > 0
        self.points_filtered = points[points[:, 2] > 0]
        self.points_filtered = points[points[:, 1] > 0]



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


        # Extract X, Y, Z from the filtered points and plot
            
        x_filtered = self.points_filtered[:, 0]
        y_filtered = self.points_filtered[:, 1]
        z_filtered = self.points_filtered[:, 2]


        x_vals = [point['x'] for point in self.coordinates.values()]
        y_vals = [point['y'] for point in self.coordinates.values()]
        z_vals = [point['z'] for point in self.coordinates.values()]

        ax.scatter(x_filtered,y_filtered,z_filtered)
        ax.scatter(x_vals, y_vals, z_vals, s=100)  # Plot random points in the dictionary
        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")
        ax.set_zlabel("Z-axis")
        plt.show()

    def checkPointsInHalfOfSphere(self):
        # Check if each point in the random_points dictionary is inside the upper hemisphere
        return {key: self._isPointInHalfOfSphere([point['x'], point['y'], point['z']]) 
                for key, point in self.coordinates.items()}

random_points = {
    1: {'x': -334.5466646080655, 'y': 479.8682744226188, 'z': -373.9556817790648},
    2: {'x': -487.8711310374162, 'y': 182.82146416069486, 'z': -498.6379434407991},
    3: {'x': 294.07588853861864, 'y': -203.45832977487652, 'z': 305.5469975076178},
    4: {'x': 475.9845402010279, 'y': 212.0278350162423, 'z': 260.38367851776263},
    5: {'x': -174.19416044797873, 'y': 437.7144297116955, 'z': 23.14836730294826},
    6: {'x': 91.13800311030138, 'y': -193.7165230182987, 'z': 266.419954616419}
}

# Create an instance of Sphere with center (0, 0, 0) and radius 500
sphere = WorkingAreaRobotChecking(0, 0, 0, 500, random_points)

# Draw the sphere and the random points
sphere.draw()

# Check if each random point is inside the sphere
results = sphere.checkPointsInHalfOfSphere()
print(results)
