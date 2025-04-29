"""
Tests for universal variable formulation of Kepler's problem.
"""

import pytest
import numpy as np
from orbiter.core.propagation.TheKeplerProblem import (
    universal_kepler, stumpff_C, stumpff_S
)
from orbiter.core.constants.AstroConstants import CELESTIAL_BODIES_KM

def test_stumpff_functions():
    """Test Stumpff C and S functions for various input values"""
    # Test z = 0 case (use series expansion)
    assert abs(stumpff_C(0.0) - 1/2) < 1e-10
    assert abs(stumpff_S(0.0) - 1/6) < 1e-10
    
    # Test positive z
    z = 1.0
    assert abs(stumpff_C(z) - (1 - np.cos(np.sqrt(z)))/z) < 1e-10
    assert abs(stumpff_S(z) - (np.sqrt(z) - np.sin(np.sqrt(z)))/(z*np.sqrt(z))) < 1e-10
    
    # Test negative z
    z = -1.0
    assert abs(stumpff_C(z) - (1 - np.cosh(np.sqrt(-z)))/z) < 1e-10
    assert abs(stumpff_S(z) - (np.sinh(np.sqrt(-z)) - np.sqrt(-z))/((-z)*np.sqrt(-z))) < 1e-10

def test_circular_orbit():
    """Test propagation of circular orbit for one period"""
    # Initial state (circular orbit at 7000 km)
    r0 = np.array([7000.0, 0.0, 0.0])  # km
    v0 = np.array([0.0, np.sqrt(CELESTIAL_BODIES_KM['earth']/7000.0), 0.0])  # km/s
    
    # Propagate for one period
    period = 2*np.pi*np.sqrt(7000.0**3/CELESTIAL_BODIES_KM['earth'])
    rf, vf = universal_kepler(r0, v0, period)
    
    # Should return to starting position/velocity
    assert np.allclose(r0, rf, rtol=1e-8)
    assert np.allclose(v0, vf, rtol=1e-8)

def test_elliptical_orbit():
    """Test propagation of elliptical orbit"""
    # Create elliptical orbit (e=0.1)
    a = 7000.0  # km
    e = 0.1
    mu = CELESTIAL_BODIES_KM['earth']
    
    # Initial state at periapsis
    r0 = np.array([a*(1-e), 0.0, 0.0])
    v0 = np.array([0.0, np.sqrt(mu*(2/np.linalg.norm(r0) - 1/a)), 0.0])
    
    # Propagate for half period
    period = 2*np.pi*np.sqrt(a**3/mu)
    rf, vf = universal_kepler(r0, v0, period/2)
    
    # Should be at apoapsis
    expected_r = a*(1+e)
    assert abs(np.linalg.norm(rf) - expected_r) < 1e-6

def test_hyperbolic_orbit():
    """Test propagation of hyperbolic orbit"""
    # Create hyperbolic orbit (e=1.5)
    rp = 7000.0  # km periapsis
    e = 1.5
    mu = CELESTIAL_BODIES_KM['earth']
    
    # Calculate a (negative for hyperbolic)
    a = rp/(1-e)
    
    # Initial state at periapsis
    r0 = np.array([rp, 0.0, 0.0])
    v0 = np.array([0.0, np.sqrt(mu*(-1/a + 2/rp)), 0.0])
    
    # Propagate forward
    dt = 10000.0  # seconds
    rf, vf = universal_kepler(r0, v0, dt)
    
    # Check that energy is conserved
    E0 = np.dot(v0, v0)/2 - mu/np.linalg.norm(r0)
    Ef = np.dot(vf, vf)/2 - mu/np.linalg.norm(rf)
    assert abs(E0 - Ef) < 1e-10

def test_convergence_failure():
    """Test that non-convergence raises appropriate error"""
    r0 = np.array([7000.0, 0.0, 0.0])
    v0 = np.array([0.0, 8.0, 0.0])
    
    with pytest.raises(RuntimeError):
        universal_kepler(r0, v0, 1000.0, max_iter=1)  # Force non-convergence

def test_different_bodies():
    """Test propagation around different celestial bodies"""
    r0 = np.array([7000.0, 0.0, 0.0])
    v0 = np.array([0.0, 8.0, 0.0])
    dt = 1000.0
    
    # Propagate around Earth and Jupiter
    r_earth, v_earth = universal_kepler(r0, v0, dt, body='earth')
    r_jupiter, v_jupiter = universal_kepler(r0, v0, dt, body='jupiter')
    
    # Motion should be different due to different gravitational parameters
    assert not np.allclose(r_earth, r_jupiter)
    assert not np.allclose(v_earth, v_jupiter)

def test_custom_mu():
    """Test propagation with custom gravitational parameter"""
    r0 = np.array([7000.0, 0.0, 0.0])
    v0 = np.array([0.0, 8.0, 0.0])
    dt = 1000.0
    
    # Use a custom mu value
    custom_mu = 5.0e5  # km³/s²
    r_custom, v_custom = universal_kepler(r0, v0, dt, mu=custom_mu)
    
    # Should be different from Earth's motion
    r_earth, v_earth = universal_kepler(r0, v0, dt, body='earth')
    assert not np.allclose(r_custom, r_earth)
    assert not np.allclose(v_custom, v_earth)