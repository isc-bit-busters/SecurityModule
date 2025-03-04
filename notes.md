working area --> https://www.universal-robots.com/developer/hardware-and-motion/robot-motion-payload-and-working-area/


find a point in 3d to check if arm is in the working area 
from sphere formula 

(x−x0​)²+(y−y0​)²+(z−z0​)²=r²

--> 

x=x0​+rcos(θ)sin(ϕ)
y=y0​+rsin(θ)sin(ϕ)
z=z0​+rcos(ϕ)



https://www.universal-robots.com/articles/ur/robot-care-maintenance/max-joint-torques-cb3-and-e-series/ --> joint force


http://perso-laris.univ-angers.fr/~boimond/UR3e_User_Manual_en_Global.pdf --> speed joint limit 30 degres/s 

https://www.bila-as.com/media/10op3oof/710-943-00_ur3e_user_manual_en_global.pdf --> for safe home position 


Mercredi --> compreansion du système d'axe du robot, simulateur et ro bot pphysiqueont un système d'axes différents 
        --> test d'un dessign sur le cube 
        --> test d'une inverse kinématique à nous ( elle est pas encore fini )

Jeudi --> hand eye calibration pour la camera 
      --> generation d'une texture sur un cube, la texture est prise d'une image