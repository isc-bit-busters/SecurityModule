import unittest
from workingAreaChecking import WorkingAreaRobotChecking


class TestWorkingAreaRobotChecking(unittest.TestCase):
    def setUp(self):
        """
        Set up multiple sets of test points and their expected results.
        """
        self.test_cases = [
            # (test_points, expected_results)
            (
                {
                    1: {"x": 100, "y": 200, "z": 300},  # Inside
                    2: {"x": -100, "y": 200, "z": 300},  # Inside
                    3: {"x": 100, "y": -200, "z": 300},  # Outside (y < 0)
                    4: {"x": 100, "y": 200, "z": -300},  # Outside (z < 0)
                    5: {"x": 600, "y": 200, "z": 300},  # Outside (exceeds radius)
                    6: {"x": 0, "y": 300, "z": 400},  # Inside
                },
                {1: True, 2: True, 3: False, 4: False, 5: False, 6: True},
            ),
            (
                {
                    1: {"x": 0, "y": 0, "z": 0},  # Inside
                    2: {"x": -50, "y": 50, "z": 50},  # Inside
                    3: {"x": 50, "y": -50, "z": 50},  # Outside (y < 0)
                    4: {"x": 50, "y": 50, "z": -50},  # Outside (z < 0)
                    5: {"x": 300, "y": 300, "z": 300},  # Outside (exceeds radius)
                    6: {"x": 0, "y": 100, "z": 100},  # Inside
                },
                {1: True, 2: True, 3: False, 4: False, 5: False, 6: True},
            ),
            (
                {
                    1: {"x": 150, "y": 150, "z": 150},  # Inside
                    2: {"x": -150, "y": 150, "z": 150},  # Inside
                    3: {"x": 150, "y": -150, "z": 150},  # Outside (y < 0)
                    4: {"x": 150, "y": 150, "z": -150},  # Outside (z < 0)
                    5: {"x": 700, "y": 150, "z": 150},  # Outside (exceeds radius)
                    6: {"x": 0, "y": 200, "z": 200},  # Inside
                },
                {1: True, 2: True, 3: False, 4: False, 5: False, 6: True},
            ),
            (
                {
                    1: {
                        "x": -334.5466646080655,
                        "y": 479.8682744226188,
                        "z": -373.9556817790648,
                    },
                    2: {
                        "x": -487.8711310374162,
                        "y": 182.82146416069486,
                        "z": -498.6379434407991,
                    },
                    3: {
                        "x": 294.07588853861864,
                        "y": -203.45832977487652,
                        "z": 305.5469975076178,
                    },
                    4: {
                        "x": 475.9845402010279,
                        "y": 212.0278350162423,
                        "z": 260.38367851776263,
                    },
                    5: {
                        "x": -174.19416044797873,
                        "y": 437.7144297116955,
                        "z": 23.14836730294826,
                    },
                    6: {
                        "x": 91.13800311030138,
                        "y": -193.7165230182987,
                        "z": 266.419954616419,
                    },
                },
                {1: False, 2: False, 3: False, 4: False, 5: True, 6: False},
            ),
            (
                {
                    1: {"x": 250, "y": 250, "z": 250},  # Inside
                    2: {"x": -250, "y": 250, "z": 250},  # Inside
                    3: {"x": 250, "y": -250, "z": 250},  # Outside (y < 0)
                    4: {"x": 250, "y": 250, "z": -250},  # Outside (z < 0)
                    5: {"x": 800, "y": 250, "z": 250},  # Outside (exceeds radius)
                    6: {"x": 0, "y": 400, "z": 400},  # Outside
                },
                {1: True, 2: True, 3: False, 4: False, 5: False, 6: False},
            ),
            (
                {
                    1: {"x": 50, "y": 50, "z": 50},  # Inside
                    2: {"x": -50, "y": 50, "z": 50},  # Inside
                    3: {"x": 50, "y": -50, "z": 50},  # Outside (y < 0)
                    4: {"x": 50, "y": 50, "z": -50},  # Outside (z < 0)
                    5: {"x": 400, "y": 250, "z": 250},  # Outside (exceeds radius)
                    6: {"x": 0, "y": 100, "z": 100},  # Inside
                },
                {1: True, 2: True, 3: False, 4: False, 5: False, 6: True},
            ),
        ]

    def test_points_in_half_sphere(self):
        """
        Loop through multiple test cases to check if points are classified correctly.
        """
        for i, (test_points, expected_results) in enumerate(self.test_cases, start=1):
            with self.subTest(f"Test Case {i}"):
                sphere = WorkingAreaRobotChecking(0, 0, 0, 500, test_points)
                results = sphere.checkPointsInHalfOfSphere()
                self.assertEqual(results, expected_results)


if __name__ == "__main__":
    unittest.main()
