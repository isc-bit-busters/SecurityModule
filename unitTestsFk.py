import unittest

from forwardKinematics import ForwardKinematic



class TestForwardKinematics(unittest.TestCase):
    def setUp(self):
        self.exptedMatrices = {
            1: [
                [0.64278761, 4.69259e-17, -0.766044443, 0.0],
                [-0.766044443, 3.93755e-17, -0.64278761, 0.0],
                [0.0, 1.0, 6.12574e-17, 0.15185],
                [0.0, 0.0, 0.0, 1.0],
            ],
            2: [
                [-0.984807753, 0.173648178, 0.0, 0.239849928],
                [-0.173648178, -0.984807753, 0.0, 0.042292014],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ],
            3: [
                [0.515038075, -0.857167301, 0.0, -0.109806118],
                [0.857167301, 0.515038075, 0.0, -0.182748069],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ],
            4: [
                [-0.945518576, 1.994353e-17, -0.325568154, 0.0],
                [-0.325568154, -5.92e-17, 0.945518576, 0.0],
                [0.0, 1.0, 6.12574e-17, 0.13105],
                [0.0, 0.0, 0.0, 1.0],
            ],
            5: [
                [-0.5, -5.30505e-17, -0.866025404, 0.0],
                [0.866025404, -3.06287e-17, -0.5, 0.0],
                [0.0, -1.0, 6.12574e-17, 0.08535],
                [0.0, 0.0, 0.0, 1.0],
            ],
            6: [
                [6.12574e-17, -1.0, 0.0, 0.0],
                [1.0, 6.12574e-17, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0921],
                [0.0, 0.0, 0.0, 1.0],
            ],
        }

        self.exptedMatricesDotProd = {
            1: [
                [-0.63302, 0.11162, -0.76604, 0.15417],
                [0.75441, -0.13302, -0.64279, -0.18374],
                [-0.17365, -0.98481, 0.00000, 0.19409],
                [0.0, 0.0, 0.0, 1.0],
            ],
            2: [
                [-0.23035, 0.60009, -0.76604, 0.20328],
                [0.27453, -0.71516, -0.64279, -0.24226],
                [-0.93358, -0.35837, 0.00000, 0.39313],
                [0.0, 0.0, 0.0, 1.0],
            ],
            3: [
                [0.02243, -0.76604, 0.64240, 0.10289],
                [-0.02673, -0.64279, -0.76558, -0.32650],
                [0.99939, -0.0, -0.03490, 0.39313],
                [0.0, 0.0, 0.0, 1.0],
            ],
            4: [
                [-0.67463, -0.64240, 0.36359, 0.15772],
                [-0.54330, 0.76558, 0.34455, -0.39184],
                [-0.49970, 0.03490, -0.86550, 0.39015],
                [0.0, 0.0, 0.0, 1.0],
            ],
            5: [
                [-0.64240, 0.67463, 0.36359, 0.19121],
                [0.76558, 0.54330, 0.34455, -0.36011],
                [0.03490, 0.49970, -0.86550, 0.31044],
                [0.0, 0.0, 0.0, 1.0],
            ],
        }
        self.tolerance = 1e-4
    
    

        self.angles = [
               [
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
            ],
         
        ]
        self.coordinates_test = [
            
             {       1: {
                "x": 0.0,
                "y": 0.0,
                "z": 0.1518,
            },
            2: {
                "x": 0.15417,
                "y": -0.18374,
                "z": 0.19409,
            },
            3: {
                "x": 0.20328,
                "y": -0.24226,
                "z": 0.39313,
            },
            4: {
                "x": 0.10289,
                "y": -0.32650,
                "z": 0.39313,
            },
            5: {
                "x": 0.15772,
                "y": -0.39184,
                "z": 0.39015,
            },
            6: {
                "x": 0.19121,
                "y": -0.36011,
                "z": 0.31044,
            }},
                {1: {
                    "x": 0.0,
                    "y": 0.0,
                    "z": 0.1518,
                },
                2: {
                    "x": -0.24355,
                    "y": 0.0,
                    "z": 0.15180,
                },
                3: {
                    "x": -0.45675,
                    "y": 0.0,
                    "z": 0.15180,
                },
                4: {
                    "x": -0.45675,
                    "y": -0.13105,
                    "z": 0.15180,
                },
                5: {
                    "x": -0.45675,
                    "y": -0.13105,
                    "z": 0.06645,
                },
                6: {
                    "x": -0.45675,
                    "y":-0.22315,
                    "z": 0.06645,
                },
            },
            {1: {
                    "x": 0.0,
                    "y": 0.0,
                    "z": 0.1518,
                },
                2: {
                    "x": -0.12169,
                    "y": 0.00007,
                    "z": -0.05917,
                },
                3: {
                    "x": -0.32758,
                    "y": 0.00019,
                    "z": -0.11451,
                },
                4: {
                    "x": -0.32751,
                    "y": 0.13124,
                    "z":-0.11451,
                },
                5: {
                    "x": -0.40992,
                    "y": 0.13129,
                    "z": -0.13670,
                },
                6: {
                    "x": -0.40987,
                    "y":0.22339,
                    "z": -0.13668,
                },
                },{1: {
                    "x": 0.0,
                    "y": 0.0,
                    "z": 0.1518,
                },
                2: {
                    "x": 0.0,
                    "y": -0.00019,
                    "z": 0.39535,
                },
                3: {
                    "x": -0.00012,
                    "y": -0.15101,
                    "z": 0.54605,
                },
                4: {
                    "x": 0.13093,
                    "y": -0.15111,
                    "z": 0.54605,
                },
                5: {
                    "x": 0.13086,
                    "y": -0.23646,
                    "z": 0.54598,
                },
                6: {
                    "x": 0.21065,
                    "y": -0.23656,
                    "z": 0.59198,
                },
                },
              
        ]

    def test_buildMatrices(self):
        fk = ForwardKinematic(self.angles[0])
        for i, (mat_fk, mat_test) in enumerate(
            zip(fk.matrices, self.exptedMatrices.values())
        ):
            self.assertEqual(len(mat_fk), len(mat_test))
            for j, (row_fk, row_test) in enumerate(zip(mat_fk, mat_test)):
                for elem_fk, elem_test in zip(row_fk, row_test):
                    self.assertAlmostEqual(elem_fk, elem_test, delta=self.tolerance)

    def test_getDotProdMat(self):
        fk = ForwardKinematic(self.angles[0])
        matDot = fk._getDotProdMat()
        for i, (mat_fk, mat_test) in enumerate(
            zip(matDot[1:], list(self.exptedMatricesDotProd.values()))
        ):
            self.assertEqual(len(mat_fk), len(mat_test))
            for j, (row_fk, row_test) in enumerate(zip(mat_fk, mat_test)):
                for elem_fk, elem_test in zip(row_fk, row_test):
                    self.assertAlmostEqual(elem_fk, elem_test, delta=self.tolerance)



    def test_getCoordinates(self):
        for angles_test, coordinates_test in zip(self.angles, self.coordinates_test):
            fk = ForwardKinematic(angles_test)
            coordinates = fk.getCoordinates()
            for coords_fk, coords_test in zip(
                coordinates.values(), coordinates_test.values()
            ):
                for key in ["x", "y", "z"]:
                    fk_value = coords_fk.get(key)
                    test_value = coords_test.get(key)
                    self.assertAlmostEqual(fk_value, test_value, delta=self.tolerance)


if __name__ == "__main__":
    unittest.main()
