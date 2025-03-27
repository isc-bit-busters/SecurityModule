import math
import plotly.graph_objects as go

from security.globalRobotChecking import GlobalRobotChecking



class Interpolation:
    def __init__(self, logs=True, stopAtFirstError=True,):
        self.anglesDistanceVariation = 0.1  # Threshold for skipping interpolation
        self.t = 0.1
        self.logs = logs
        self.stopAtFirstError = stopAtFirstError

    def _getLinearInterpolation(self, theta1, theta2, t):
        """Performs linear interpolation between two angles without wrapping."""
        diff = theta2 - theta1  # No wrapping
        return theta1 + t * diff

    def _getAngleDistance(self, theta1, theta2):
        """Calculates the shortest distance between two angles."""
        return ((theta2 - theta1 + math.pi) % (2 * math.pi)) - math.pi

    def _isTooClose(self, theta1, theta2):
        """Check if two angles are too close to interpolate."""

        return (
            abs(self._getAngleDistance(theta1, theta2)) < self.anglesDistanceVariation
        )

    def _getInterpSingleTrajectory(self, angles1: list[float], angles2: list[float]):
        """
        Interpolates between two sets of 6 angles (angles1 and angles2).
        Generates multiple interpolated angles if needed.
        """

        def interpolate_recursive(theta1, theta2):
            """Generates an array of interpolated values between theta1 and theta2."""
            if self._isTooClose(theta1, theta2):
                return [theta1]

            # Create multiple steps from theta1 to theta2
            steps = [theta1]
            num_steps = int(1 / self.t)  # Number of interpolation points
            for i in range(1, num_steps + 1):
                interpolated_angle = self._getLinearInterpolation(
                    theta1, theta2, i * self.t
                )
                steps.append(interpolated_angle)

            return steps

        # Interpolating each angle independently
        interpolated_angles_per_joint = [
            interpolate_recursive(angles1[i], angles2[i]) for i in range(6)
        ]

        # Transpose the list to get step-wise interpolation
        max_steps = max(len(lst) for lst in interpolated_angles_per_joint)
        interpolated_trajectory = [
            [
                interpolated_angles_per_joint[j][i]
                if i < len(interpolated_angles_per_joint[j])
                else interpolated_angles_per_joint[j][-1]
                for j in range(6)
            ]
            for i in range(max_steps)
        ]


        return interpolated_trajectory
    
    def _isTrajectoriesSafe(self, angles1, angles2):
        """Check if two trajectories are safe."""
        interpolated_trajectory = self._getInterpSingleTrajectory(angles1, angles2)
        for i in range(len(interpolated_trajectory)):
            positions = GlobalRobotChecking(interpolated_trajectory[i],self.logs).checkNextBehaviour()
            if not positions:
                if self.logs:
                    print(f"Unsafe trajectory between angles {angles1} and angles {angles2}")
                return False 
    
        return True


    def getAllInterpolatedAngles(self, angles: list[list[float]]):
        """Interpolates between all sets of angles in the list."""
        allnotSafePositions = {}
        for i in range(len(angles) - 1):
            isSafe = self._isTrajectoriesSafe(angles[i], angles[i + 1])
            if not isSafe:
                if self.stopAtFirstError:
                    return (i, i+1), (angles[i], angles[i+1])
                allnotSafePositions[(i,i+1)] = (angles[i], angles[i+1])
        return allnotSafePositions
                
     

    def drawTrajectory(self, trajectory):
        """Draws a trajectory of joint angles."""
        # Plot angles variation
        fig_angles = go.Figure()

        num_angles = len(trajectory[0])  # Number of angles (joints)
        angle_steps = list(range(len(trajectory)))

        # Prepare lists for each angle
        angles = [[] for _ in range(num_angles)]

        # Collect angle values over all steps
        for step in trajectory:
            for i, angle in enumerate(step):
                angles[i].append(angle)

        # Plot each angle's variation over steps
        for i in range(num_angles):
            fig_angles.add_trace(
                go.Scatter(
                    x=angle_steps,
                    y=angles[i],
                    mode="lines+markers",
                    name=f"Angle {i + 1}",
                )
            )

        fig_angles.update_layout(
            title="Joint Angles Variation",
            xaxis_title="Step",
            yaxis_title="Angle (radians)",
        )

        fig_angles.show()
    



if __name__ == "__main__":
    angles = [
        [0.9509, -1.6623, 0.6353, -0.5976, -1.5722, 0.0],  # First set of angles
        [0.9509, -1.6623, 1.6353, -0.5976, -1.5722, 0.0],  # Second set of angles
        [0.9509, -1.6623, 0.6353, -0.7, -1.5722, 0.0],  # First set of angles
        [0.9509, 1.6623, 1.8353, -0.5976, -1.5722, 0.0],
    ]

    interpolation = Interpolation(True, False)
    res = interpolation.getAllInterpolatedAngles(angles)
    print(res)
