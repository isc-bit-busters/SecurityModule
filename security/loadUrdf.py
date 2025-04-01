import os
import pybullet as p

def loadRobot():
    package_path = os.path.dirname(os.path.abspath(__file__))
    urdf_path = os.path.join(package_path, "urdf", "iscoin_azz.urdf")

    if not os.path.exists(urdf_path):
        raise FileNotFoundError(f"URDF file not found at {urdf_path}")
    print(f"Loading URDF from: {urdf_path}")
    robot_id =  p.loadURDF(urdf_path, useFixedBase=True, flags=p.URDF_USE_SELF_COLLISION)
    return robot_id

def loadPlane(): 
    package_path = os.path.dirname(os.path.abspath(__file__))
    urdf_path = os.path.join(package_path, "urdf", "plane.urdf")

    if not os.path.exists(urdf_path):
        raise FileNotFoundError(f"URDF file not found at {urdf_path}")

    plane_id = p.loadURDF(urdf_path, basePosition=[0, 0, 0])
    return plane_id