import math

def lerp_angle_radians(theta1, theta2, t):
    """
    Linearly interpolates between two angles in radians, ensuring the shortest path.

    Parameters:
    - theta1: Starting angle in radians.
    - theta2: Ending angle in radians.
    - t: Interpolation factor (0.0 to 1.0).

    Returns:
    - Interpolated angle in radians.
    """
    diff = (theta2 - theta1 + math.pi) % (2 * math.pi) - math.pi  # Wrap to [-π, π]
    return (theta1 + t * diff) % (2 * math.pi)





def angle_distance_radians(theta1, theta2):
    """Returns the shortest distance between two angles (in radians)."""
    return ((theta2 - theta1 + math.pi) % (2 * math.pi)) - math.pi



angle1_deg = 20  # Angle 1 in degrees
angle2_deg = 10  # Angle 2 in degrees

# Convert degrees to radians
angle1_rad = math.radians(angle1_deg)
angle2_rad = math.radians(angle2_deg)


print("angle1_rad", angle1_rad)
print("angle2_rad", angle2_rad)
t = 0.5  # Interpolation factor (e.g., 25% of the way)
interp_angle_rad = lerp_angle_radians(angle2_rad, angle1_rad, t)
print(interp_angle_rad)  # Output the interpolated angle in radians
print(math.degrees(angle_distance_radians(angle2_rad, angle1_rad)))  # Output in degrees
