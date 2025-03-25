import math
import numpy as np
import plotly.graph_objects as go

from .forwardKinematics import ForwardKinematic

class Interpolation():
    def __init__(self):
        self.t = 0.1  # Step size for interpolation (smaller = more points)

    def _getLinearInterpolation(self, theta1, theta2, t):
        """Performs linear interpolation between two angles, considering wrapping."""
        diff = (theta2 - theta1 + math.pi) % (2 * math.pi) - math.pi  # Wrap to [-π, π]
        return (theta1 + t * diff) % (2 * math.pi)

    def getInterpolatedTrajectory(self, angles1: list[float], angles2: list[float]):
        """
        Interpolates between two sets of 6 angles (angles1 and angles2).
        Generates multiple interpolated angles if needed.
        """
        def interpolate_recursive(theta1, theta2):
            """Generates an array of interpolated values between theta1 and theta2."""
            steps = [theta1]
            num_steps = int(1 / self.t)  # Number of interpolation points
            for i in range(1, num_steps + 1):
                interpolated_angle = self._getLinearInterpolation(theta1, theta2, i * self.t)
                steps.append(interpolated_angle)
            return steps

        # Interpolating each angle independently
        interpolated_angles_per_joint = [interpolate_recursive(angles1[i], angles2[i]) for i in range(6)]

        # Transpose the list to get step-wise interpolation
        max_steps = max(len(lst) for lst in interpolated_angles_per_joint)
        interpolated_trajectory = [
            [interpolated_angles_per_joint[j][i] if i < len(interpolated_angles_per_joint[j]) else interpolated_angles_per_joint[j][-1] for j in range(6)]
            for i in range(max_steps)
        ]

        return interpolated_trajectory

    def drawTrajectory(self, trajectory):

        fig = go.Figure()

        # Convert trajectory to joint positions using FK
        all_joint_positions = [ForwardKinematic(angles).getCoordinates() for angles in trajectory]

        # Debug print to check the structure of output
        print("DEBUG: Joint positions ->", all_joint_positions)

        num_joints = len(all_joint_positions[0])  # Number of joints in the arm

        # Prepare lists for each joint
        joint_x = [[] for _ in range(num_joints)]
        joint_y = [[] for _ in range(num_joints)]
        joint_z = [[] for _ in range(num_joints)]

        # Collect joint positions over all steps
        for joints in all_joint_positions:
            for i, joint in enumerate(joints.values()):
                joint_x[i].append(joint["x"])
                joint_y[i].append(joint["y"])
                joint_z[i].append(joint["z"])

        # Plot each joint's motion separately
        for i in range(num_joints):
            fig.add_trace(go.Scatter3d(
                x=joint_x[i], y=joint_y[i], z=joint_z[i],
                mode='lines+markers',
                name=f'Joint {i + 1}',
                line=dict(width=2)
            ))

        fig.update_layout(
            title="Robot Arm Interpolated Motion",
            scene=dict(
                xaxis_title="X Position",
                yaxis_title="Y Position",
                zaxis_title="Z Position"
            )
        )

        fig.show()




if __name__ == "__main__":
    angles = [
        [0.9509, -1.6623, 0.6353, -0.5976, -1.5722, 0.0],  # First set of angles
        [0.9509, -1.6623, 1.8353, -0.5976, -1.5722, 0.0],  # Second set of angles
    ]

    interpolation = Interpolation()
    result = interpolation.getInterpolatedTrajectory(angles[0], angles[1])
    interpolation.drawTrajectory(result)

    # Printing step-wise interpolated angles
    for i, step in enumerate(result):
        print(f"Step {i}: {step}")
