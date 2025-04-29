"""
Unit conversion functions for astrodynamics calculations.
Provides standard conversions between common units used in orbital mechanics.
"""

def meters_to_kilometers(meters: float) -> float:
    """
    Convert meters to kilometers.
    
    Parameters
    ----------
    meters : float
        Length in meters
        
    Returns
    -------
    float
        Length in kilometers
    """
    return meters * 1e-3

def cubic_meters_to_cubic_kilometers(cubic_meters: float) -> float:
    """
    Convert cubic meters to cubic kilometers.
    
    Parameters
    ----------
    cubic_meters : float
        Volume in cubic meters
        
    Returns
    -------
    float
        Volume in cubic kilometers
    """
    return cubic_meters * 1e-9