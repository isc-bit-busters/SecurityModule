import pytest

from .collisonWithItselfCheck import RobotCollisonWithItselfChecking

# Define multiple sets of angles for testing
test_angles = [
    {
        "angles": [0.9509, -1.6623, 1.8353, -0.5976, -1.5722, 0.0],
        "expected": {
            (1, 3): True,
            (1, 4): True,
            (1, 5): False,
            (2, 4): True,
            (2, 5): True,
            (3, 5): True,
        },
    },
    {
        "angles": [0.9509, -1.6623, 0.6353, -0.5976, -1.5722, 0.0],
        "expected": {
            (1, 3): True,
            (1, 4): True,
            (1, 5): True,
            (2, 4): True,
            (2, 5): True,
            (3, 5): True,
        },  # Expected safe result
    },
    {
        "angles": [0.9509, -1.6623, 2.6353, 0.5976, 1.5722, 0.0],
        "expected": {
            (1, 3): False,
            (1, 4): False,
            (1, 5): False,
            (2, 4): True,
            (2, 5): True,
            (3, 5): True,
        },
    },
    {
        "angles": [0.9509, -1.6623, 0.6353, -0.5976, -1.5722, 0.0],
        "expected": {
            (1, 3): True,
            (1, 4): True,
            (1, 5): True,
            (2, 4): True,
            (2, 5): True,
            (3, 5): True,
        },
    },
    {
        "angles": [0.0, -3.14, 3.14, 0.0, 0.0, 0.0],
        "expected": {
            (1, 3): False,
            (1, 4): False,
            (1, 5): False,
            (2, 4): True,
            (2, 5): True,
            (3, 5): True,
        },
    },
    {
        "angles": [0.0, -3.14, 2.7, 0.0, 3.14, 0.0],
        "expected": {
            (1, 3): False,
            (1, 4): False,
            (1, 5): False,
            (2, 4): True,
            (2, 5): False,
            (3, 5): True,
        },
    },
    {
        "angles": [0.9509, -1.6623, 0.6353, 0.5, -1.5722, 0.0],
        "expected": {
            (1, 3): True,
            (1, 4): True,
            (1, 5): False,
            (2, 4): True,
            (2, 5): True,
            (3, 5): True,
        },
    },
    {
        "angles": [0.00001, 0.000001, 0.00001, 0.00001, 0.00001, 0.000001],
        "expected": {
            (1, 3): True,
            (1, 4): True,
            (1, 5): True,
            (2, 4): True,
            (2, 5): True,
            (3, 5): True,
        },
    },
    {
        "angles": [0.0, -3.14, 3.14, 0.0, 3.14, 0.0],
        "expected": {
            (1, 3): False,
            (1, 4): False,
            (1, 5): False,
            (2, 4): True,
            (2, 5): False,
            (3, 5): True,
        },
    },
    {
        "angles": [-0.7493, -1.0, 1.0478, -1.0997, -0.2, -2.3201],
        "expected": {
            (1, 3): True,
            (1, 4): True,
            (1, 5): True,
            (2, 4): True,
            (2, 5): True,
            (3, 5): True,
        },
    },
    {
        "angles": [0.9019, -1.1795, 1.9326, -2.3253, -1.5697, -0.6689],
        "expected": {
            (1, 3): True,
            (1, 4): True,
            (1, 5): True,
            (2, 4): True,
            (2, 5): True,
            (3, 5): True,
        },

    },
    {
        "angles": [0.0, -3.14, 2.2, 0.6, 3.0, 0.0],
        "expected": {
            (1, 3): True,
            (1, 4): False,
            (1, 5): False,
            (2, 4): True,
            (2, 5): False,
            (3, 5): True,
        },
    }

]


@pytest.mark.parametrize("test_case", test_angles)
def test_checkingCollisonWithItself(test_case):
    angles = test_case["angles"]
    expected = test_case["expected"]
    print(angles)
    robot = RobotCollisonWithItselfChecking(angles)
    result = robot.checkingCollisonWithItself()
    print("res", result)

    assert result == expected


if __name__ == "__main__":
    pytest.main()
