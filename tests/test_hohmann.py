"""
Tests for Hohmann transfer calculations.
Tests include edge cases, known transfers, and error conditions.
"""

import pytest
import numpy as np
from orbiter.core.maneuvers.Hohmann import hohmann_delta_v
from orbiter.core.constants.AstroConstants import EARTH_MASS, GRAVITATIONAL_CONSTANT

def test_leo_to_geo():
    """Test LEO to GEO transfer (classic textbook case)"""
    r1 = 6_771_000  # LEO radius in meters (≈400km altitude)
    r2 = 42_164_000  # GEO radius in meters
    dv1, dv2, dv_total, a_transfer = hohmann_delta_v(r1, r2)
    
    # Expected values from textbook calculations
    expected_dv1 = 2.4547e3  # m/s (approx)
    expected_dv2 = 1.4772e3  # m/s (approx)
    expected_total = 3.9319e3  # m/s (approx)
    
    assert abs(dv1 - expected_dv1) < 1.0  # Within 1 m/s
    assert abs(dv2 - expected_dv2) < 1.0
    assert abs(dv_total - expected_total) < 1.0
    assert abs(a_transfer - (r1 + r2)/2) < 1.0

def test_reverse_transfer():
    """Test that lowering orbit gives same total ΔV as raising it"""
    r1 = 8000e3  # 8000 km in meters
    r2 = 12000e3  # 12000 km in meters
    
    up_dv1, up_dv2, up_total, _ = hohmann_delta_v(r1, r2)
    down_dv1, down_dv2, down_total, _ = hohmann_delta_v(r2, r1)
    
    assert abs(up_total - down_total) < 1e-10

def test_invalid_radii():
    """Test that invalid radii raise appropriate errors"""
    with pytest.raises(ValueError):
        hohmann_delta_v(-1000, 42164e3)
    
    with pytest.raises(ValueError):
        hohmann_delta_v(6771e3, -42164e3)
    
    with pytest.raises(ValueError):
        hohmann_delta_v(0, 42164e3)

def test_same_orbit():
    """Test transfer to same orbit requires no ΔV"""
    r = 7000e3  # 7000 km in meters
    dv1, dv2, dv_total, a_transfer = hohmann_delta_v(r, r)
    
    assert abs(dv1) < 1e-10
    assert abs(dv2) < 1e-10
    assert abs(dv_total) < 1e-10
    assert abs(a_transfer - r) < 1e-10

def test_custom_body():
    """Test transfer around different celestial body"""
    r1 = 6771e3
    r2 = 42164e3
    jupiter_mass = 1.899e27  # kg
    
    earth_dv1, earth_dv2, earth_total, _ = hohmann_delta_v(r1, r2)
    jupiter_dv1, jupiter_dv2, jupiter_total, _ = hohmann_delta_v(r1, r2, jupiter_mass)
    
    # Larger body should require more ΔV
    assert jupiter_total > earth_total
    # Both should be positive
    assert jupiter_total > 0
    assert earth_total > 0