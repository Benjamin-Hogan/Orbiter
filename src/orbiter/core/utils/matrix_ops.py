"""
Utility functions for matrix operations, particularly for coordinate transformations.
"""

import numpy as np

def invert_rotation(matrix: np.ndarray) -> np.ndarray:
    """
    Returns the inverse of a rotation matrix (its transpose)
    
    Parameters
    ----------
    matrix : np.ndarray
        3x3 rotation matrix
        
    Returns
    -------
    np.ndarray
        Inverse of the rotation matrix
    """
    return matrix.T

def combine_rotations(*matrices: np.ndarray) -> np.ndarray:
    """
    Combines multiple rotation matrices in order
    
    Parameters
    ----------
    *matrices : np.ndarray
        Variable number of 3x3 rotation matrices
        
    Returns
    -------
    np.ndarray
        Combined rotation matrix
    """
    result = matrices[0]
    for matrix in matrices[1:]:
        result = result @ matrix
    return result