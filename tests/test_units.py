"""
Tests for unit conversion functions.
"""

import pytest
from orbiter.core.constants.conversions.units import (
    meters_to_kilometers,
    cubic_meters_to_cubic_kilometers
)

def test_meters_to_kilometers():
    """Test conversion from meters to kilometers"""
    # Basic conversions
    assert meters_to_kilometers(1000.0) == 1.0
    assert meters_to_kilometers(0.0) == 0.0
    assert meters_to_kilometers(1.0) == 0.001
    
    # Large numbers
    assert meters_to_kilometers(1_000_000.0) == 1000.0
    
    # Small numbers
    assert meters_to_kilometers(0.1) == 0.0001
    
    # Negative numbers
    assert meters_to_kilometers(-1000.0) == -1.0

def test_cubic_meters_to_cubic_kilometers():
    """Test conversion from cubic meters to cubic kilometers"""
    # Basic conversions
    assert cubic_meters_to_cubic_kilometers(1_000_000_000.0) == 1.0
    assert cubic_meters_to_cubic_kilometers(0.0) == 0.0
    
    # Small numbers (typical for small bodies)
    assert cubic_meters_to_cubic_kilometers(1.0) == 1e-9
    
    # Large numbers (typical for planetary bodies)
    assert cubic_meters_to_cubic_kilometers(1e12) == 1000.0
    
    # Negative numbers (though physically meaningless)
    assert cubic_meters_to_cubic_kilometers(-1e9) == -1.0

def test_conversion_precision():
    """Test that conversions maintain sufficient precision"""
    # Test a precise value typical in astrodynamics
    value_m3 = 3.986004418e14  # Earth's gravitational parameter in m³/s²
    value_km3 = cubic_meters_to_cubic_kilometers(value_m3)
    
    # Should maintain at least 9 significant figures
    assert abs(value_km3 - 3.986004418e5) < 1e-4

def test_conversion_types():
    """Test that conversions work with different numeric types"""
    # Integer input
    assert meters_to_kilometers(1000) == 1.0
    
    # Float input
    assert meters_to_kilometers(1000.0) == 1.0
    
    # Scientific notation
    assert meters_to_kilometers(1e3) == 1.0
    
    # Different numeric types for cubic conversion
    assert cubic_meters_to_cubic_kilometers(1e9) == 1.0
    assert cubic_meters_to_cubic_kilometers(1_000_000_000) == 1.0

def test_error_handling():
    """Test error handling for invalid inputs"""
    # Test with non-numeric types
    with pytest.raises((TypeError, ValueError)):
        meters_to_kilometers("1000")
    
    with pytest.raises((TypeError, ValueError)):
        cubic_meters_to_cubic_kilometers("1e9")
    
    # Test with None
    with pytest.raises((TypeError, ValueError)):
        meters_to_kilometers(None)
    
    with pytest.raises((TypeError, ValueError)):
        cubic_meters_to_cubic_kilometers(None)