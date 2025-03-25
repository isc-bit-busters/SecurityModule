

# UR3e Robot Safety and Motion Analysis

## 1. Checking if a Point is in the Working Area
To verify if a point \((x, y, z)\) is within the robot's workspace, use the **sphere formula**:

\[
(x - x_0)^2 + (y - y_0)^2 + (z - z_0)^2 = r^2
\]

Alternatively, using **spherical coordinates**, a point in the workspace can be expressed as:

\[
x = x_0 + r \cos(\theta) \sin(\phi)
\]

\[
y = y_0 + r \sin(\theta) \sin(\phi)
\]

\[
z = z_0 + r \cos(\phi)
\]

🔗 [UR3e Working Area](https://www.universal-robots.com/developer/hardware-and-motion/robot-motion-payload-and-working-area/)

---

## 2. Forward Kinematics (FK) for the UR3e
Forward kinematics allows us to compute the **positions of all joints and the end-effector**.

- **DH Parameters for UR3e**:  
  🔗 [Denavit-Hartenberg Parameters](https://www.universal-robots.com/articles/ur/application-installation/dh-parameters-for-calculations-of-kinematics-and-dynamics/)

- Excel sheet with full FK calculations available.

---

## 3. Joint Limits & Forces

### **Max Joint Torques**  
🔗 [UR3e Torque Specs](https://www.universal-robots.com/articles/ur/robot-care-maintenance/max-joint-torques-cb3-and-e-series/)

### **Joint Speed Limits**  
- Maximum Speed: **30°/s**
- Formula for **angular velocity**:

\[
\omega = \frac{d\theta}{dt}
\]

🔗 [Angular Velocity](https://en.wikipedia.org/wiki/Angular_velocity)

---

## 4. Safe Home Position
To ensure a **safe starting position**, refer to:

🔗 [UR3e Safe Home Position Guide](https://www.bila-as.com/media/10op3oof/710-943-00_ur3e_user_manual_en_global.pdf)

---

## 5. Collision Checking & Distance Between Joints
To compute the **distance between two joints**, model them as **cylinders**.

- Use this approach for calculating the distance:  
  🔗 [Distance Between Cylinders](https://www.researchgate.net/figure/Distance-between-two-cylinders_fig1_282996677)

- Consider **diameters** of robot links to improve accuracy.

---

## 6. Safety Parameters

### **Checking Safe Angles**
- Using the **Jacobian matrix**:  
  🔗 [Jacobian Robotics](https://www.rosroboticslearning.com/jacobian)

- A simpler approach: Compute **distance from obstacles**.

- **Safety Parameters (User Manual, Section 22):**  
  🔗 [UR3e Safety Parameters](https://www.universal-robots.com/manuals/EN/PDF/SW10_6/user-manual-UR3e-PolyX-PDF_online/708-825-00_UR3e%20PolyScope%20X_User_Manual_PolyScopeX_en_Global.pdf)

---

## 7. Computing Joint Speeds
- **Joint Speed Limit**: **1.15°/s**  
  🔗 [UR3e User Manual](https://s3-eu-west-1.amazonaws.com/ur-support-site/61565/99454_UR3e_User_Manual_en_US.pdf)

- Formula for **angular speed**:

\[
\omega = \frac{\Delta \theta}{\Delta t}
\]

---

## 8. Distance btw 2 joints 

Compute distance with 2 joint interpreted with cylinders --> https://www.researchgate.net/figure/Distance-between-two-cylinders_fig1_282996677 --> similar to the distance between 2 point but this approach simplifies things too much (robotic arm is in 3d not 2d) so we have to know diameters of each part of the robotic arm to compute the distance between 2 joint. 
there are methods in the control library such as get_tcp_force which checks that the robot is not exerting too much force on itself. Useful if the manual implementation takes too long but not advisable as a first choice because we would like to stop the robot before they make contact, not when they are already in contact (only then does the tcp force come into action).

## 9. Interpolation btw two trajectories

this part of interpolation is necessary to check that the final trajectory of the robot has no problems at the safety level. For the moment the interpolation will be done only on the final trajectory if there is time it will be applied to all possible trajectories. This step is necessary because the robot movej is blocking so we would not be able to stop the robot in time if it does something dangerous

DIfferent type of interpolation: 
- Linear interp. --> I start with this one for algorithmic simplicity with the risk that it is not accurate enough 
- Polynomial interp.