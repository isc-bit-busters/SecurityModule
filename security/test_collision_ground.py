import pytest
import numpy as np
from robotPositionChecking import DistanceFromGroundChecking

# filepath: /home/marta/Projects/SecurityModule/test_unitTestsCollisonWithTheGround.py


# Test data
angles = [
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

results_test_maths = [-0.66, -0.37318136069134724, -0.60, -0.93126]

@pytest.mark.parametrize("index, expected_result", enumerate(results_test_maths, start=2))
def test_computeDistanceFromGround(index, expected_result):
    # Use the first set of angles for testing
    robot_position = DistanceFromGroundChecking(angles[0])
    result = robot_position._computeDistanceFromGround(index)
    assert pytest.approx(result, abs=0.1) == expected_result