import numpy as np

""" This class allow to find actual position of each joint, knowing angles of each joint """


class ForwardKinematics:
    def __init__(self, angles: list):
        self.numJoints = len(angles)
        # DH parameters as numpy arrays
        self.alpha = np.array([np.pi/2, 0, 0, np.pi/2, -np.pi/2, 0])
        self.a = np.array([0, -0.24355, -0.2132, 0, 0, 0])
        self.d = np.array([0.15185, 0, 0, 0.13105, 0.08535, 0.0921])
        
        # Current angles as numpy array
        self.angles = np.array(angles)
        print(self.angles[5])
        
        # Create joints dictionary with numpy arrays
        self.joints = {
            i+1: {
                "angle": self.angles[i],
                "alpha": self.alpha[i],
                "a": self.a[i],
                "d": self.d[i]
            }
            for i in range(self.numJoints)
        }
        
        # Declare transformation matrices as a 3D numpy array (6x4x4)
        self.matrices = np.zeros((self.numJoints, 4, 4))
        self._buildMatrices()



    def _buildMatrices(self):
        for i in range(self.numJoints):
            theta = self.angles[i]
            alpha = self.alpha[i]
            a = self.a[i]
            d = self.d[i]
            # Compute transformation matrix using DH convention
            self.matrices[i] = np.array([
                [np.cos(theta), -np.sin(theta) * np.cos(alpha),  np.sin(theta) * np.sin(alpha), a * np.cos(theta)],
                [np.sin(theta),  np.cos(theta) * np.cos(alpha), -np.cos(theta) * np.sin(alpha), a * np.sin(theta)],
                [0,             np.sin(alpha),                 np.cos(alpha),                 d],
                [0,             0,                             0,                             1]
            ])
  # do dot prod of mat  
    def _getDotProdMat(self):
        matricesDotProd = np.zeros((self.numJoints, 4, 4))
        
        matricesDotProd[0] = self.matrices[0]

        for j in range(1, self.numJoints):  
            matricesDotProd[j] = np.dot(matricesDotProd[j-1], self.matrices[j]) 

        print("Final Dot Product Matrices:\n", matricesDotProd)
        return matricesDotProd

    
# fill a dict with final coords of each joint 
    def getCoordinates(self):
        finalDotProdMat = self._getDotProdMat()
        finalCoordinates = {
            i+1:{
                "x" : finalDotProdMat[i][0][3],
                "y" : finalDotProdMat[i][1][3],
                "z" : finalDotProdMat[i][2][3]
            }
             
            for i in range(1,len(finalDotProdMat))

        }
        finalCoordinates[1] = { "x": self.matrices[0][0][3] ,"y":  self.matrices[0][1][3] , "z":  self.matrices[0][2][3]}
    
        return finalCoordinates



# Example usage
test = ForwardKinematics([5.410520681, 3.316125579, 1.029744259,3.473205211, 2.094395102, 1.570796327])
print(test.joints)
print(test.getCoordinates())
