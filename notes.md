working area --> https://www.universal-robots.com/developer/hardware-and-motion/robot-motion-payload-and-working-area/


find a point in 3d to check if arm is in the working area 
from sphere formula 

(x−x0​)²+(y−y0​)²+(z−z0​)²=r²

--> 

x=x0​+rcos(θ)sin(ϕ)
y=y0​+rsin(θ)sin(ϕ)
z=z0​+rcos(ϕ)


forward kinematics implmentation --> to have positions from  [here](https://www.universal-robots.com/articles/ur/application-installation/dh-parameters-for-calculations-of-kinematics-and-dynamics/) way to do fk with good params for ur3e in exel doc there is entiere processus to compute fk  

https://www.universal-robots.com/articles/ur/robot-care-maintenance/max-joint-torques-cb3-and-e-series/ --> joint force


http://perso-laris.univ-angers.fr/~boimond/UR3e_User_Manual_en_Global.pdf --> speed joint limit 30 degres/s 

https://www.bila-as.com/media/10op3oof/710-943-00_ur3e_user_manual_en_global.pdf --> for safe home position 

to check safe angles --> https://www.rosroboticslearning.com/jacobian
to check safe angles --> approche plus naif distance d'un obstacles --> https://www.universal-robots.com/manuals/EN/PDF/SW10_6/user-manual-UR3e-PolyX-PDF_online/708-825-00_UR3e%20PolyScope%20X_User_Manual_PolyScopeX_en_Global.pdf --> Tool force 


paragraph 22 --> Param to garantee safety of robot





Joint Speed limit p.l-15 --> 1.15 degrees/s --> https://s3-eu-west-1.amazonaws.com/ur-support-site/61565/99454_UR3e_User_Manual_en_US.pdf
Compute speed of each joint with angular speed formula of angular speed --> https://en.wikipedia.org/wiki/Angular_velocity

Compute distance with 2 joint interpreted with cylinders --> https://www.researchgate.net/figure/Distance-between-two-cylinders_fig1_282996677 --> similar to the distance between 2 point but this approach simplifies things too much (robotic arm is in 3d not 2d) so we have to know diameters of each part of the robotic arm to compute the distance between 2 joint 

