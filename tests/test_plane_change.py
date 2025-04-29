"""
Tests for orbital plane change maneuver calculations.
"""

import pytest
import numpy as np
from orbiter.core.maneuvers.PlaneChange import plane_change_delta_v

def test_no_inclination_change():
    """Test that zero inclination change requires no ΔV"""
    v = 7.5  # km/s
    delta_i = 0.0  # radians
    
    delta_v = plane_change_delta_v(v, delta_i)
    assert abs(delta_v) < 1e-10

def test_90_degree_change():
    """Test 90-degree plane change (maximum efficiency loss case)"""
    v = 7.5  # km/s
    delta_i = np.pi / 2  # 90 degrees in radians
    
    delta_v = plane_change_delta_v(v, delta_i)
    expected = v * np.sqrt(2)  # For 90 degrees, ΔV = v√2
    
    assert abs(delta_v - expected) < 1e-10

def test_invalid_inputs():
    """Test that invalid inputs raise appropriate errors"""
    with pytest.raises(ValueError):
        plane_change_delta_v(-1.0, np.pi/4)  # Negative velocity
    
    with pytest.raises(ValueError):
        plane_change_delta_v(7.5, -np.pi/4)  # Negative inclination
    
    with pytest.raises(ValueError):
        plane_change_delta_v(7.5, 3*np.pi)  # Inclination > 2π

def test_typical_leo_change():
    """Test a typical LEO inclination change"""
    v = 7.5  # km/s
    delta_i = np.radians(28.5)  # Cape Canaveral to equatorial
    
    delta_v = plane_change_delta_v(v, delta_i)
    # Hand calculation: 2 * 7.5 * sin(28.5°/2) ≈ 3.7 km/s
    expected = 3.7  # km/s (approximate)
    
    assert abs(delta_v - expected) < 0.1

def test_small_angle():
    """Test that small angle approximation holds for small changes"""
    v = 7.5  # km/s
    delta_i = np.radians(1.0)  # 1 degree
    
    delta_v = plane_change_delta_v(v, delta_i)
    # For small angles, ΔV ≈ v * Δi
    small_angle_approx = v * delta_i
    
    # Should be within 0.1% for 1 degree
    assert abs(delta_v - small_angle_approx) / small_angle_approx < 0.001