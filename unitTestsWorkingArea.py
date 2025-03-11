import unittest
import numpy as np
from workingAreaChecking import WorkingAreaRobotChecking

class TestWorkingAreaRobotChecking(unittest.TestCase):

    def setUp(self):
        """
        Set up the test data for the WorkingAreaRobotChecking class.
        """
        self.test_cases = [
            # Test case 1: Points inside the upper hemisphere
            {
                "test_points": {
                    1: {"x": 0.1, "y": 0.1, "z": 0.1},  # Inside
                    2: {"x": -0.2, "y": -0.2, "z": 0.2},  # Inside
                    3: {"x": 0.3, "y": -0.3, "z": 0.3},  # Outside (y < 0)
                    4: {"x": -0.3, "y": 0.3, "z": -0.3},  # Outside (z < 0)
                    5: {"x": 0.6, "y": 0.6, "z": 0.6},  # Outside (exceeds radius)
                    6: {"x": 0.2, "y": 0.2, "z": 0.2},  # Inside
                },
                "expected_results": {
                    1: True,
                    2: True,
                    3: False,
                    4: False,
                    5: False,
                    6: True,
                }
            },
            # Test case 2: Points in the bottom hemisphere
            {
                "test_points": {
                    1: {"x": -0.1, "y": 0.1, "z": -0.1},  # Inside (bottom hemisphere)
                    2: {"x": 0.1, "y": -0.1, "z": -0.1},  # Inside (bottom hemisphere)
                    3: {"x": 0.3, "y": -0.3, "z": -0.3},  # Inside (bottom hemisphere)
                    4: {"x": 0.5, "y": -0.5, "z": -0.5},  # Outside (exceeds radius)
                    5: {"x": 0, "y": 0, "z": -0.6},  # Outside (exceeds radius)
                },
                "expected_results": {
                    1: False,  # Bottom hemisphere
                    2: False,  # Bottom hemisphere
                    3: False,  # Bottom hemisphere
                    4: False,  # Outside (exceeds radius)
                    5: False,  # Outside (exceeds radius)
                }
            },
            # Test case 3: Points on the boundary (edge of the sphere)
            {
                "test_points": {
                    1: {"x": 0.5, "y": 0, "z": 0},  # On the boundary
                    2: {"x": -0.5, "y": 0, "z": 0},  # On the boundary
                    3: {"x": 0, "y": 0.5, "z": 0},  # On the boundary
                    4: {"x": 0, "y": -0.5, "z": 0},  # On the boundary
                    5: {"x": 0, "y": 0, "z": 0.5},  # On the boundary
                    6: {"x": 0, "y": 0, "z": -0.5},  # On the boundary (z < 0)
                },
                "expected_results": {
                    1: True,  # On the boundary is considered inside
                    2: True,  # On the boundary is considered inside
                    3: True,  # On the boundary is considered inside
                    4: True,  # On the boundary is considered inside
                    5: True,  # On the boundary is considered inside
                    6: False,  # Bottom hemisphere, not inside the upper hemisphere
                }
            },
            # Test case 4: Random scattered points
            {
                "test_points": {
                    1: {"x": -0.3, "y": 0.4, "z": 0.1},  # Inside
                    2: {"x": 0.2, "y": 0.5, "z": -0.3},  # Outside (z < 0)
                    3: {"x": -0.7, "y": -0.2, "z": 0.2},  # Outside (exceeds radius)
                    4: {"x": 0.2, "y": -0.1, "z": 0.3},  # Inside
                    5: {"x": 0.1, "y": 0.1, "z": 0.4},  # Inside
                    6: {"x": -0.1, "y": -0.2, "z": -0.3},  # Outside (z < 0)
                },
                "expected_results": {
                    1: True,
                    2: False,
                    3: False,
                    4: True,
                    5: True,
                    6: False,
                }
            },
            # Test case 5: Extreme points (further from the origin)
            {
                "test_points": {
                    1: {"x": 1000, "y": 0, "z": 0},  # Outside (exceeds radius)
                    2: {"x": 0, "y": 1000, "z": 0},  # Outside (exceeds radius)
                    3: {"x": 0, "y": 0, "z": 1000},  # Outside (exceeds radius)
                    4: {"x": -0.5, "y": 0, "z": 0},  # Inside
                    5: {"x": 0, "y": 0, "z": -0.5},  # Inside
                    6: {"x": 0, "y": -0.5, "z": 0},  # Inside
                },
                "expected_results": {
                    1: False,  # Outside (exceeds radius)
                    2: False,  # Outside (exceeds radius)
                    3: False,  # Outside (exceeds radius)
                    4: True,   # Inside
                    5: True,   # Inside
                    6: True,   # Inside
                }
            },
        ]

    def test_points_in_half_sphere(self):
        """
        Loop through multiple test cases to check if points are classified correctly.
        """
        for i, case in enumerate(self.test_cases, start=1):
            with self.subTest(f"Test Case {i}"):
                # Set up WorkingAreaRobotChecking instance for the test case
                test_points = case["test_points"]
                expected_results = case["expected_results"]
                # Assume the angles in the test case are just placeholders; adjust them as necessary.
                angles = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # Dummy angles for testing
                
                # Create WorkingAreaRobotChecking instance with a dummy center (0, 0, 0) and radius
                sphere = WorkingAreaRobotChecking(0, 0, 0, 0.5, angles, True, test_points)
                
                # Check if the computed results match the expected results
                results = sphere.checkPointsInHalfOfSphere()
                
                # Compare the actual results with expected results
                self.assertEqual(results, expected_results, f"Failed on test case {i}")

if __name__ == "__main__":
    unittest.main()
