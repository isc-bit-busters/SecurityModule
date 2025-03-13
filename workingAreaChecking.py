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
        print(self.coordinates)
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
        if randomPoint[1] >0:
            return False
        # Check if the point is within the sphere's radius
        print((randomPoint[0] - self.x0)**2 + (randomPoint[1] - self.y0)**2 + (randomPoint[2] - self.z0)**2 )
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
        if not self.coordinates:
            return None  # Return None if the dictionary is empty
        
        latest_key = next(reversed(self.coordinates))  # Get the last added key
        latest_point = self.coordinates[latest_key]   # Get the corresponding point
        
        # Check if it's inside the upper hemisphere
        return {latest_key: self._isPointInHalfOfSphere([latest_point['x'], latest_point['y'], latest_point['z']])}




if __name__ == "__main__": 
    pos1 = [0.35230425000190735,-0.7322418850711365,0.5806735197650355,-1.0719731015018006,4.915554523468018,0.31385645270347595]
    pos2 = [2.711972236633301,-1.102702186708786,0.9782894293414515,-1.2463486355594178,4.384324073791504,-0.8515551725970667]

    inside_pos1 = [0.9481282830238342, -1.3380088073066254, 0.7121437231646937, -1.0540800851634522, -1.5575674215899866, -0.5976246039019983]
    inside_pos2 = [0.6118811368942261, -1.0608138006976624, 0.6223252455340784, -1.2109331053546448, -1.4435485045062464, -1.4143388907061976]

    out_pos1 = [2.807316541671753, -1.4116303038648148, 0.6609633604632776, -0.6375070375255127, -1.1185200850116175, -1.4017718474017542]
    out_pos2 = [2.807316541671753, -1.4116303038648148, 0.6609633604632776, -0.6375070375255127, -1.1185200850116175, -1.4017718474017542]

    limit_pos1 = [2.063770055770874, -0.9286156457713624, 0.6224730650531214, -1.5671449464610596, -1.461837116871969, -0.4172404448138636]

    home1 = [   0.9509,
                -1.6623,
                0.6353,
                -0.5976,
                -1.5722,
                0.0]
    inside= [
                1.1193,
                -1.5922,
                1.1245,
                -1.1035,
                -1.572,
                -0.4507
            ]
    outside = [
                -0.7493,
                -1.5177,
                1.0478,
                -1.0997,
                -1.5695,
                -2.3201
            ]
    home2= [
                0.9509,
                -1.6623,
                0.6353,
                -0.5976,
                -1.5722,
                0.0
            ]
    test = WorkingAreaRobotChecking(0, 0, 0, 1, outside, False ) # Inside)
    print(test.checkPointsInHalfOfSphere()) 
    test.draw()