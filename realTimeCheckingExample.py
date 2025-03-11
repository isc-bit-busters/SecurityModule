import time

from globalRobotChecking import GlobalRobotChecking


interval = 0.01 # in case of need you cam change the interval
checking_task = GlobalRobotChecking([0.0, 0.0, 0.0, 0.0, 0.0, 0.0],interval)  #change with the first angle detected by the robot
checking_task.start()  # Start the task
# HERE the code to run waypoints of the robot
time.sleep(10)  # Run for 10 seconds
checking_task.stop()  # Stop the task """