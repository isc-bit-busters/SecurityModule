import unittest

from robotPositionChecking import RobotPositonChecking
import numpy as np
class TestCollisionsWithTheGround(unittest.TestCase): 
    def setUp(self):
        self.angles  = [ [
            5.410520681,
            3.316125579,
            1.029744259,
            3.473205211,
            2.094395102,
            1.570796327,
        ],
            [
                0.000,  # Joint 1
                0.000,  # Joint 2
                0.000,  # Joint 3
                0.000,  # Joint 4
                0.000,  # Joint 5
                0.000,  # Joint 6
            ],
            [
                3.141,  # Joint 1 (π)
                2.094,  # Joint 2 (π/3)
                0.785,  # Joint 3 (π/4)
                4.712,  # Joint 4 (3π/2)
                6.283,  # Joint 5 (2π)
                9.425,  # Joint 6 (3π)
            ],
       
            [
                1.570,  # Joint 1
                -1.570,  # Joint 2
                0.785,  # Joint 3
                -0.785,  # Joint 4
                0.523,  # Joint 5
                -0.523,  # Joint 6
            ],]
        self.results_test = [[]]
        self.test_coordinateds_maths = {1: {'x': np.float64(0.0), 'y': np.float64(-0.0), 'z': np.float64(0.15185)}, 2: {'x': np.float64(0.1541725620215664), 'y': np.float64(-0.18373570473672415), 'z': np.float64(0.19414201372133497)}, 3: {'x': np.float64(0.2032841365831819), 'y': np.float64(-0.24226460018017104), 'z': np.float64(0.39318136069134724)}, 4: {'x': np.float64(0.10289401229707314), 'y': np.float64(-0.32650191641127874), 'z': np.float64(0.39318136069134724)}, 5: {'x': np.float64(0.1577225143711653), 'y': np.float64(-0.3918439807588445), 'z': np.float64(0.39020268865336755)}, 6: {'x': np.float64(0.19120958666770654), 'y': np.float64(-0.36011123729478767), 'z': np.float64(0.3104903371559329)}} #tested with the forwardKinematics.py
        self.results_test_maths = [-0.66, -0.37318136069134724, -0.60, -0.93126] #tested with the forwardKinematics.py

    def test_computeDistanceFromGround(self):
        for i in range(len(self.results_test_maths)):
            self.robotPosition = RobotPositonChecking(self.angles[0])
            results = self.robotPosition._computeDistanceFromGround(i+2)
            self.assertAlmostEqual(results, self.results_test_maths[i],delta=0.1)


if __name__ == "__main__":
    unittest.main()