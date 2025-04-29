"""
Tests for orbital state vector to classical orbital elements conversions and vice versa.
"""

import pytest
import numpy as np
from orbiter.core.states.states import StateRV, ClassicalOE

def test_circular_equatorial():
    """Test conversion of circular equatorial orbit state vectors"""
    # Create a simple circular equatorial orbit
    r = np.array([7000e3, 0, 0])  # 7000 km circular orbit
    v = np.array([0, np.sqrt(3.986004418e14 / 7000e3), 0])  # Circular velocity
    state = StateRV(r, v)
    
    coe = state.as_coe()
    
    # For circular equatorial orbit:
    assert abs(coe.e) < 1e-10  # eccentricity ≈ 0
    assert abs(coe.i) < 1e-10  # inclination ≈ 0
    assert abs(coe.a - 7000e3) < 1e-6  # semimajor axis = radius

def test_inclined_orbit():
    """Test conversion of inclined circular orbit"""
    inc = np.pi/4  # 45 degrees
    r = 7000e3
    v = np.sqrt(3.986004418e14 / r)
    
    # Rotate position and velocity to desired inclination
    r_vec = np.array([r * np.cos(inc), 0, r * np.sin(inc)])
    v_vec = np.array([0, v, 0])
    
    state = StateRV(r_vec, v_vec)
    coe = state.as_coe()
    
    assert abs(coe.i - inc) < 1e-10
    assert abs(coe.e) < 1e-10  # Still circular

def test_elliptical_orbit():
    """Test conversion of elliptical orbit"""
    # Create an elliptical orbit with e=0.1
    a = 7000e3  # semimajor axis
    e = 0.1     # eccentricity
    
    # Periapsis position and velocity
    r_peri = a * (1 - e)
    v_peri = np.sqrt(3.986004418e14 * (2/r_peri - 1/a))
    
    state = StateRV(np.array([r_peri, 0, 0]), np.array([0, v_peri, 0]))
    coe = state.as_coe()
    
    assert abs(coe.e - e) < 1e-10
    assert abs(coe.a - a) < 1e-6

def test_roundtrip_conversion():
    """Test that converting rv->coe->rv gives original state"""
    r = np.array([6500e3, 1000e3, -200e3])
    v = np.array([-1.0e3, 7.0e3, 1.0e3])
    original = StateRV(r, v)
    
    # Convert to COE and back
    coe = original.as_coe()
    final = coe.as_rv()
    
    # Check that we got back to where we started
    assert np.allclose(original.r, final.r, rtol=1e-10)
    assert np.allclose(original.v, final.v, rtol=1e-10)

def test_edge_cases():
    """Test edge cases in orbital elements conversion"""
    # Test nearly circular orbit (e ≈ 0)
    r = np.array([7000e3, 1e-6, 0])
    v = np.array([0, np.sqrt(3.986004418e14 / 7000e3), 0])
    state = StateRV(r, v)
    coe = state.as_coe()
    
    assert abs(coe.e) < 1e-6
    
    # Test nearly equatorial orbit (i ≈ 0)
    r = np.array([7000e3, 0, 1e-6])
    state = StateRV(r, v)
    coe = state.as_coe()
    
    assert abs(coe.i) < 1e-6