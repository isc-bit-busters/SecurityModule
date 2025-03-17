import pytest
from collisonWithItselfCheck import RobotCollisonWithItselfChecking

# Define multiple sets of angles for testing
test_angles = [
    {
        "angles": [
            0.9509, -1.6623, 1.8353, -0.5976, -1.5722, 0.0
        ],
        "expected": False  # Expected collision result
    },
    {
        "angles": [
            0.9509, -1.6623, 0.6353, -0.5976, -1.5722, 0.0
        ],
        "expected": True  # Expected safe result
    },
    {
        "angles": [
            0.9509, -1.6623, 2.6353, 0.5976, 1.5722, 0.0
        ],
        "expected": False  # Expected collision result
    },
    {
        "angles": [
            0.9509, -1.6623, 0.6353, -0.5976, -1.5722, 0.0
        ],
        "expected": True  # Expected safe result
    },
    {
        "angles": [
                0.0,
                -3.14,
                3.14,
                0.0,
                0.0,
                0.0
            ],
        "expected": False  # Expected safe result
    }
]

@pytest.mark.parametrize("test_case", test_angles)
def test_checkingCollisonWithItself(test_case):
    angles = test_case["angles"]
    expected = test_case["expected"]
    print(angles)
    robot = RobotCollisonWithItselfChecking(angles)
    result = robot.checkingCollisonWithItself()
    print("res",result)
    # Check if any collision is detected
    if False in result.values() :
        collision_detected = False 
    else: 
        collision_detected = True
    print("col",collision_detected)
    assert collision_detected == expected

if __name__ == "__main__":
    pytest.main()