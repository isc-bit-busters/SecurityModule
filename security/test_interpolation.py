import numpy as np
import pytest
from .interpolation import Interpolation

@pytest.mark.parametrize(
    "angles1, angles2, expected_middle",
    [
        # Test case 1: Two sets of angles far apart
        (
            [0.0, -1.0, 0.5, -0.5, -1.5, 0.0],
            [1.0, 0.0, 1.5, 0.5, 0.0, 1.0],
            [0.5, -0.5, 1.0, 0.0, -0.75, 0.5],  # Expected middle step
        ),
        # Test case 2: Two sets of angles very close
        (
            [0.1, -0.1, 0.1, -0.1, 0.1, -0.1],
            [0.11, -0.09, 0.11, -0.09, 0.11, -0.09],
            [0.105, -0.095, 0.105, -0.095, 0.105, -0.095],  # Expected middle step
        ),
        # Test case 3: Identical sets of angles
        (
            [0.5, -0.5, 0.5, -0.5, 0.5, -0.5],
            [0.5, -0.5, 0.5, -0.5, 0.5, -0.5],
            [0.5, -0.5, 0.5, -0.5, 0.5, -0.5],  # No interpolation needed
        ),
        # Test case 4: Angles at boundaries of [-π, π]
        (
            [-3.14159, 3.14159, -3.14159, 3.14159, -3.14159, 3.14159],
            [3.14158, -3.14158, 3.14158, -3.14158, 3.14158, -3.14158],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Expected middle step
        ),
        (
            [0.9509, -1.6623, 0.6353, -0.5976, -1.5722, 0.0],   
            [ 0.0, -1.0, 2.0, 0.0, 0.0, 0.0],  
            [0.47545, -1.33115, 1.31765, -0.2988, -0.7861, 0.0],  # Expected middle step
        )
    ],
)
def test_getInterpolatedTrajectory(angles1, angles2, expected_middle):
    interpolation = Interpolation()
    result = interpolation._getInterpSingleTrajectory(angles1, angles2)
    
    # Verify the structure of the result
    assert isinstance(result, list), "Result should be a list"
    assert all(isinstance(step, list) for step in result), "Each step should be a list"
    assert all(len(step) == 6 for step in result), "Each step should contain 6 angles"
    
    # Verify the first and last steps match the input angles

    assert result[0] == angles1, "First step should match angles1"
    print(f"result[0]: {result[0]}, angles1: {angles1}, angles2: {angles2}")

    if len(result) == 1:
        assert np.allclose(result[0], angles1, rtol=0.1) or np.allclose(result[0], angles2, rtol=0.1), "Single step should match either angles1 or angles2"
    else:
        assert result[-1] == pytest.approx(angles2, abs=0.1), "Last step should match angles2"
    
    # Verify the middle step matches the expected middle angles
        middle_index = len(result) // 2
        assert result[middle_index] == pytest.approx(expected_middle, abs=1e-2), "Middle step should match expected angles"