"""
Tests for coordinate frame transformations.
Tests include transformations between Topocentric-Horizon, ENU, ECEF, and GCRF frames.
"""

import pytest
import numpy as np
from orbiter.core.constants.conversions.frames.TopocentricHorizon import (
    topo_to_gcrf,
    gcrf_to_topo,
    topo_to_ecef,
    ecef_to_topo
)

def test_topo_gcrf_roundtrip():
    """Test roundtrip conversion between topocentric and GCRF frames"""
    # Test vector in topocentric frame
    r_topo = np.array([1000.0, 2000.0, 3000.0])  # meters
    
    # Observer parameters
    alt = np.radians(45)  # 45° altitude
    az = np.radians(180)  # South
    lat = np.radians(40)  # 40°N
    lst = np.radians(30)  # 30° LST
    
    # Convert to GCRF and back
    r_gcrf = topo_to_gcrf(r_topo, alt, az, lat, lst)
    r_topo_back = gcrf_to_topo(r_gcrf, alt, az, lat, lst)
    
    assert np.allclose(r_topo, r_topo_back, rtol=1e-10)

def test_topo_ecef_roundtrip():
    """Test roundtrip conversion between topocentric and ECEF frames"""
    r_topo = np.array([1000.0, 2000.0, 3000.0])  # meters
    
    # Observer parameters
    alt = np.radians(30)  # 30° altitude
    az = np.radians(90)   # East
    lat = np.radians(-35) # 35°S
    lon = np.radians(145) # 145°E
    
    # Convert to ECEF and back
    r_ecef = topo_to_ecef(r_topo, alt, az, lat, lon)
    r_topo_back = ecef_to_topo(r_ecef, alt, az, lat, lon)
    
    assert np.allclose(r_topo, r_topo_back, rtol=1e-10)

def test_zenith_observation():
    """Test observation directly overhead (alt=90°)"""
    r_topo = np.array([0.0, 0.0, 1000.0])  # Looking straight up
    alt = np.radians(90)  # 90° altitude
    az = 0.0  # Azimuth irrelevant at zenith
    lat = np.radians(45)  # 45°N
    lon = np.radians(-75) # 75°W
    
    # In ECEF, should point along the local vertical
    r_ecef = topo_to_ecef(r_topo, alt, az, lat, lon)
    
    # Vector should point outward along Earth radius direction at observer's location
    expected_direction = np.array([
        np.cos(lat) * np.cos(lon),
        np.cos(lat) * np.sin(lon),
        np.sin(lat)
    ])
    expected_direction = expected_direction / np.linalg.norm(expected_direction)
    actual_direction = r_ecef / np.linalg.norm(r_ecef)
    
    assert np.allclose(actual_direction, expected_direction, rtol=1e-10)

def test_horizon_observation():
    """Test observation along horizon (alt=0°)"""
    r_topo = np.array([1000.0, 0.0, 0.0])  # Looking along horizon
    alt = 0.0  # 0° altitude
    az = np.radians(90)  # Looking East
    lat = 0.0  # Equator
    lon = 0.0  # Prime meridian
    
    r_ecef = topo_to_ecef(r_topo, alt, az, lat, lon)
    
    # At equator, prime meridian, looking east should align with Y axis
    assert np.allclose(r_ecef / np.linalg.norm(r_ecef), [0, 1, 0], rtol=1e-10)

def test_pole_observation():
    """Test observations from poles"""
    r_topo = np.array([1000.0, 0.0, 0.0])
    alt = np.radians(45)
    az = 0.0  # Looking toward prime meridian
    lat = np.radians(90)  # North pole
    lst = np.radians(0)  # LST = 0
    
    r_gcrf = topo_to_gcrf(r_topo, alt, az, lat, lst)
    
    # Convert back
    r_topo_back = gcrf_to_topo(r_gcrf, alt, az, lat, lst)
    assert np.allclose(r_topo, r_topo_back, rtol=1e-10)

def test_error_handling():
    """Test error handling for invalid inputs"""
    r_topo = np.array([1000.0, 0.0, 0.0])
    
    # Test invalid altitude
    with pytest.raises(ValueError):
        topo_to_gcrf(r_topo, np.pi, 0, 0, 0)  # alt > π/2
    
    # Test invalid latitude
    with pytest.raises(ValueError):
        topo_to_ecef(r_topo, 0, 0, np.pi, 0)  # |lat| > π/2
    
    # Test invalid vector shape
    with pytest.raises(ValueError):
        topo_to_gcrf(np.array([1.0, 2.0]), 0, 0, 0, 0)  # Wrong shape