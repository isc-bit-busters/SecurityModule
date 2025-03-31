import math
import time
import pybullet as p
import pybullet_data

# Reconnect with GUI for visualization
# Use with DIRECT for no visu
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

robot_id = p.loadURDF("security/iscoin_azz.urdf", useFixedBase=True, flags=p.URDF_USE_SELF_COLLISION)
ground_id = p.loadURDF("plane.urdf", basePosition=[0, 0, 0])

FPS = 60

# Set the simulation time step (in seconds)
time_step = 1 /  FPS  # You can adjust this value based on your needs
p.setTimeStep(time_step)

# Set up camera for better visualization
# p.resetDebugVisualizerCamera(
#     cameraDistance=2.0, cameraYaw=0, cameraPitch=-30, cameraTargetPosition=[0, 0, 0]
# )

# Get number of joints and print their info
num_joints = p.getNumJoints(robot_id)
print(f"Number of joints: {num_joints}")
for i in range(num_joints):
    joint_info = p.getJointInfo(robot_id, i)
    print(f"Joint {i}: {joint_info[1].decode('utf-8')}")  # Joint name

mapping = {0: 2, 1: 3, 2: 4, 3: 5, 4: 6, 5: 7}

angles =[  1.5,-3.9,-3, 0.0, 0.0, 0.0]

path = [
[0.5565805435180664, -1.7810882329940796, 1.2320417165756226, -1.0197296142578125, -1.5603995323181152, 2.127431869506836], [0.5818618535995483, -1.799845576286316, 1.2450264692306519, -1.0142204761505127, -1.5603517293930054, 2.152714490890503], [0.6087886691093445, -1.8171454668045044, 1.2565603256225586, -1.0087363719940186, -1.5603082180023193, 2.179642915725708], [0.6374369859695435, -1.8329265117645264, 1.2667053937911987, -1.003401279449463, -1.5602703094482422, 2.2082927227020264], [0.667872428894043, -1.8471264839172363, 1.2755199670791626, -0.9983367323875427, -1.5602394342422485, 2.238729953765869], [2.123605489730835, -0.8311632871627808, 1.3667057752609253, -0.5492687821388245, -2.5887038707733154, -1.5747177600860596], [2.123664379119873, -0.8088163733482361, 1.3790029287338257, -0.5839115977287292, -2.5886447429656982, -1.5747162103652954], [2.1237235069274902, -0.7853255271911621, 1.389315128326416, -0.617713212966919, -2.58858585357666, -1.5747146606445312], [2.1237823963165283, -0.7607402205467224, 1.39765465259552, -0.6506367921829224, -2.588526964187622, -1.574713110923767], [2.1238412857055664, -0.7351101636886597, 1.4040312767028809, -0.6826421022415161, -2.588467836380005, -1.574711561203003]
]


path = [angles]

print(path)

def isArrived(robot_id, target_angles, tolerance=0.01):

    joint_positions = [p.getJointState(robot_id, mapping[i])[0] for i in mapping]



    for i, a in enumerate(joint_positions):
        if abs(target_angles[i] - a) > tolerance:
            return False
    return True

def check_collision(robot_id, ground_id):
    contact_points_robot = p.getContactPoints(robot_id, robot_id)  # Self-collision check
    contact_points_ground = p.getContactPoints(robot_id, ground_id)  # Ground collision check

    isInCollision = True

    def getLinkName(id):
        return (p.getJointInfo(robot_id, id)[12]).decode()

    # Check for self-collisions (ignore wrist-pen collision)
    if contact_points_robot:
        for contact in contact_points_robot:
            if getLinkName(contact[3]) == "wrist_3_link" and getLinkName(contact[4]) == "pen_link":
                continue
            print(f"⚠️ Self-Collision: {getLinkName(contact[3])} and {getLinkName(contact[4])} are colliding.")
            isInCollision = False

    # Check for ground collision
    if contact_points_ground:
        for contact in contact_points_ground:
            if getLinkName(contact[3]) == "base_link_inertia":
                continue
            print(f"⚠️ Collision with Ground: {getLinkName(contact[3])} touched the ground!")
            isInCollision = False  # Collision detected

    return isInCollision  # No collision

def is_valid_configuration(robot_id, joint_positions):
    # Set the robot to the desired joint configuration
    for i, joint_id in enumerate(mapping.values()):
        p.resetJointState(robot_id, joint_id, joint_positions[i])
    p.stepSimulation()

    return check_collision(robot_id, ground_id) # True if no collisions, False otherwise

# Set the joint motor control mode to position control
time.sleep(1)
isValid = is_valid_configuration(robot_id, angles)  

if not isValid:
    print("The initial configuration is not valid. Please check the configuration.")
else:
    print("The initial configuration is valid.")

currTargetIndex = 0
moving = False
currTarget = None
while p.isConnected():
    pass

    # # Step simulation


    # if not moving:
    #     if currTargetIndex > len(path) - 1:
    #         print("Done !")
    #         break
    #     currTarget = path[currTargetIndex]
    #     print("Current target : ", currTarget)  
    #     print("Setting new target position : ", currTarget)
    #     for i, a in enumerate(currTarget):
    #         p.setJointMotorControl2(
    #             bodyUniqueId=0,
    #             jointIndex=mapping[i],
    #             controlMode=p.POSITION_CONTROL,
    #             targetPosition=a,
    #             force=10
    #         )
    #     moving = True
    # if moving:
    #     if not isArrived(robot_id, currTarget):
    #         pass
    #         time.sleep(0.1)
    #     else:
    #         print("Is arrived ! Passing to point : ", currTargetIndex + 1)
    #         currTargetIndex += 1
    #         moving = False
    
    # check_collision(robot_id,ground_id)
    #p.stepSimulation()