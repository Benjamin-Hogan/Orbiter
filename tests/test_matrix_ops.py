"""
Tests for matrix operations utilities, particularly for coordinate transformations.
"""

import pytest
import numpy as np
from orbiter.core.utils.matrix_ops import invert_rotation, combine_rotations

def test_invert_rotation():
    """Test rotation matrix inversion (transpose)"""
    # Create a simple rotation matrix (45° around z-axis)
    angle = np.pi/4
    c, s = np.cos(angle), np.sin(angle)
    R = np.array([
        [c, -s, 0],
        [s, c, 0],
        [0, 0, 1]
    ])
    
    R_inv = invert_rotation(R)
    
    # Test properties of rotation matrix inverse
    assert np.allclose(R @ R_inv, np.eye(3))  # RR^T = I
    assert np.allclose(R_inv @ R, np.eye(3))  # R^TR = I
    assert np.allclose(R_inv, R.T)            # R^T = R^(-1)

def test_combine_rotations():
    """Test combining multiple rotation matrices"""
    # 90° rotation around z
    Rz = np.array([
        [0, -1, 0],
        [1, 0, 0],
        [0, 0, 1]
    ])
    
    # 90° rotation around x
    Rx = np.array([
        [1, 0, 0],
        [0, 0, -1],
        [0, 1, 0]
    ])
    
    # Combined rotation
    R = combine_rotations(Rz, Rx)
    
    # Test properties
    assert np.allclose(R @ R.T, np.eye(3))  # Result should be orthogonal
    assert abs(np.linalg.det(R) - 1.0) < 1e-10  # Determinant should be 1
    
    # Test associativity
    R1 = combine_rotations(combine_rotations(Rz, Rx), Rz)
    R2 = combine_rotations(Rz, combine_rotations(Rx, Rz))
    assert np.allclose(R1, R2)

def test_rotate_vector():
    """Test rotating vectors with rotation matrices"""
    # 90° rotation around z-axis
    angle = np.pi/2
    R = np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1]
    ])
    
    # Test vector [1, 0, 0] should become [0, 1, 0]
    v = np.array([1, 0, 0])
    v_rotated = R @ v
    assert np.allclose(v_rotated, [0, 1, 0])

def test_rotation_properties():
    """Test mathematical properties of rotation matrices"""
    # Create arbitrary rotation (30° around each axis)
    angles = [np.pi/6, np.pi/6, np.pi/6]
    c1, s1 = np.cos(angles[0]), np.sin(angles[0])
    c2, s2 = np.cos(angles[1]), np.sin(angles[1])
    c3, s3 = np.cos(angles[2]), np.sin(angles[2])
    
    Rx = np.array([[1, 0, 0], [0, c1, -s1], [0, s1, c1]])
    Ry = np.array([[c2, 0, s2], [0, 1, 0], [-s2, 0, c2]])
    Rz = np.array([[c3, -s3, 0], [s3, c3, 0], [0, 0, 1]])
    
    R = combine_rotations(Rz, Ry, Rx)
    
    # Test properties
    assert np.allclose(R @ R.T, np.eye(3))  # Orthogonality
    assert abs(np.linalg.det(R) - 1.0) < 1e-10  # Special orthogonal
    assert np.allclose(invert_rotation(R), R.T)  # Inverse = transpose

def test_error_handling():
    """Test error handling for invalid inputs"""
    # Test with non-square matrix
    with pytest.raises(ValueError):
        R = np.array([[1, 0], [0, 1], [0, 0]])
        invert_rotation(R)
    
    # Test with non-3x3 matrix
    with pytest.raises(ValueError):
        R = np.eye(4)
        invert_rotation(R)
    
    # Test combining no matrices
    with pytest.raises(ValueError):
        combine_rotations()
    
    # Test combining with invalid matrix
    with pytest.raises(ValueError):
        R1 = np.eye(3)
        R2 = np.eye(4)
        combine_rotations(R1, R2)