import pytest

from .robotPositionChecking import DistanceFromGroundChecking


# Test data
angles = [
    {
        "angles": [
            5.410520681,
            3.316125579,
            1.029744259,
            3.473205211,
            2.094395102,
            1.570796327,
        ],
        "expected_result": {1: True, 2: True, 3: True, 4: True, 5: True, 6: True},
    },
    {
        "angles": [
            0.000,  # Joint 1
            0.000,  # Joint 2
            0.000,  # Joint 3
            0.000,  # Joint 4
            0.000,  # Joint 5
            0.000,  # Joint 6
        ],
        "expected_result": {1: True, 2: True, 3: True, 4: True, 5: False, 6: False},
    },
    {
        "angles": [
            1.570,  # Joint 1
            -1.570,  # Joint 2
            0.785,  # Joint 3
            -0.785,  # Joint 4
            0.523,  # Joint 5
            -0.523,  # Joint 6
        ],
        "expected_result": {1: True, 2: True, 3: True, 4: True, 5: True, 6: True},
    },
    {
        "angles": [0.9509, -1.6623, 0.6353, -0.5976, -1.5722, 0.0],
        "expected_result": {1: True, 2: True, 3: True, 4: True, 5: True, 6: True},
    },
    {
        "angles": [0.9019, -0.28, 1.7852, -3.0774, -1.5697, -0.6689],
        "expected_result": {1: True, 2: True, 3: False, 4: False, 5: False, 6: False},
    },
    {
        "angles": [0.9509, -1.6623, 1.8353, -0.5976, -1.5722, 0.0],
        "expected_result": {1: True, 2: True, 3: True, 4: True, 5: True, 6: True},
    },
    {
        "angles": [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001],
        "expected_result": {1: True, 2: True, 3: True, 4: True, 5: False, 6: False},
    },
    {
        "angles": [
            3.141,  # Joint 1 (π)
            2.094,  # Joint 2 (π/3)
            0.785,  # Joint 3 (π/4)
            4.712,  # Joint 4 (3π/2)
            6.283,  # Joint 5 (2π)
            9.425,  # Joint 6 (3π)]
        ],
        "expected_result": {1: True, 2: False, 3: False, 4: False, 5: False, 6: False},
    },
]


# Test cases
@pytest.mark.parametrize("test_data", angles)
def test_computeDistanceFromGround(test_data):
    # Use the angles from the test data
    robot_position = DistanceFromGroundChecking(test_data["angles"])
    result = robot_position.checkDistanceFromTheGround()
    assert result == test_data["expected_result"]
