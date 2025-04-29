"""
Tests for time-of-flight calculations, including both universal formulation
and direct position-to-position calculations.
"""

import pytest
import numpy as np
from orbiter.core.time.UniversalTimeOfFlight import universal_time_of_flight
from orbiter.core.time.TimeOfFlightToPosition import time_of_flight_to_position
from orbiter.core.constants.AstroConstants import CELESTIAL_BODIES

def test_universal_circular():
    """Test universal time of flight for circular orbit"""
    # Circular orbit setup
    r0 = np.array([7_000_000.0, 0.0, 0.0])  # 7000 km in meters
    v0 = np.array([0.0, np.sqrt(CELESTIAL_BODIES['earth']/7_000_000.0), 0.0])
    
    # Various chi values
    chi_values = [10000.0, 50000.0, 100000.0]
    for chi in chi_values:
        dt = universal_time_of_flight(chi, r0, v0)
        assert dt > 0  # Time should be positive
        
        # Test with different bodies
        dt_sun = universal_time_of_flight(chi, r0, v0, body='sun')
        assert dt_sun < dt  # Sun's stronger gravity means faster motion

def test_universal_error_handling():
    """Test error handling in universal time of flight"""
    r0 = np.array([7_000_000.0, 0.0, 0.0])
    v0 = np.array([0.0, 7546.0, 0.0])
    
    with pytest.raises(ValueError):
        universal_time_of_flight(1000.0, r0, v0, body='invalid_body')

def test_position_circular():
    """Test time of flight between positions for circular orbit"""
    # Circular orbit
    r0 = np.array([7_000_000.0, 0.0, 0.0])
    v0 = np.array([0.0, np.sqrt(CELESTIAL_BODIES['earth']/7_000_000.0), 0.0])
    
    # Target 90 degrees ahead
    rf = np.array([0.0, 7_000_000.0, 0.0])
    
    dt = time_of_flight_to_position(r0, v0, rf)
    # Quarter orbit should take quarter of the period
    period = 2*np.pi*np.sqrt(7_000_000.0**3/CELESTIAL_BODIES['earth'])
    expected_dt = period/4
    
    assert abs(dt - expected_dt) < 1.0  # Within 1 second

def test_position_elliptical():
    """Test time of flight between positions for elliptical orbit"""
    # Elliptical orbit (e=0.1)
    a = 7_000_000.0  # meters
    e = 0.1
    mu = CELESTIAL_BODIES['earth']
    
    # Start at periapsis
    r0 = np.array([a*(1-e), 0.0, 0.0])
    v0 = np.array([0.0, np.sqrt(mu*(2/np.linalg.norm(r0) - 1/a)), 0.0])
    
    # Target apoapsis
    rf = np.array([-a*(1+e), 0.0, 0.0])
    
    dt = time_of_flight_to_position(r0, v0, rf)
    # Half orbit
    period = 2*np.pi*np.sqrt(a**3/mu)
    expected_dt = period/2
    
    assert abs(dt - expected_dt) < 1.0

def test_position_hyperbolic():
    """Test time of flight between positions for hyperbolic orbit"""
    # Hyperbolic orbit
    rp = 7_000_000.0  # meters periapsis
    e = 1.5
    mu = CELESTIAL_BODIES['earth']
    a = rp/(1-e)  # negative for hyperbolic
    
    # Start at periapsis
    r0 = np.array([rp, 0.0, 0.0])
    v0 = np.array([0.0, np.sqrt(mu*(-1/a + 2/rp)), 0.0])
    
    # Target position further out
    theta = np.pi/4  # 45 degrees
    r = rp*(1+e)/(1+e*np.cos(theta))
    rf = np.array([r*np.cos(theta), r*np.sin(theta), 0.0])
    
    dt = time_of_flight_to_position(r0, v0, rf)
    assert dt > 0  # Time should be positive

def test_position_parabolic():
    """Test time of flight between positions for parabolic orbit"""
    # Parabolic orbit (e=1)
    rp = 7_000_000.0  # meters periapsis
    mu = CELESTIAL_BODIES['earth']
    
    # Start at periapsis
    r0 = np.array([rp, 0.0, 0.0])
    v0 = np.array([0.0, np.sqrt(2*mu/rp), 0.0])
    
    # Target position
    theta = np.pi/6  # 30 degrees
    r = 2*rp/(1+np.cos(theta))
    rf = np.array([r*np.cos(theta), r*np.sin(theta), 0.0])
    
    dt = time_of_flight_to_position(r0, v0, rf)
    assert dt > 0
    
    # Test Barker's equation directly (special case for parabolic orbits)
    D0 = np.tan(0/2)
    Df = np.tan(theta/2)
    p = 2*rp
    expected_dt = 0.5*np.sqrt(2*p**3/mu)*((Df + Df**3/3) - (D0 + D0**3/3))
    
    assert abs(dt - expected_dt) < 1.0

def test_position_error_handling():
    """Test error handling in time of flight to position"""
    r0 = np.array([7_000_000.0, 0.0, 0.0])
    v0 = np.array([0.0, 7546.0, 0.0])
    rf = np.array([0.0, 7_000_000.0, 0.0])
    
    with pytest.raises(ValueError):
        time_of_flight_to_position(r0, v0, rf, body='invalid_body')