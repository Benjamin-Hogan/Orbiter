"""
Coordinate transformations from Topocentric-Horizon (Alt/Az) frame to other common reference frames.
"""

import numpy as np
from orbiter.core.constants.RotationMatrices import (
    create_topo_to_enu_matrix,
    create_enu_to_ecef_matrix,
    create_lst_rotation_matrix,
    create_topo_to_hadec_matrix
)
from orbiter.core.utils.matrix_ops import invert_rotation, combine_rotations

def get_topo_to_gcrf_matrix(alt: float, az: float, lat: float, lst: float) -> np.ndarray:
    """
    Get the rotation matrix from Topocentric-Horizon to GCRF/ECI.
    
    Parameters
    ----------
    alt : float
        Altitude angle in radians
    az : float
        Azimuth angle in radians
    lat : float
        Observer's geodetic latitude in radians
    lst : float
        Local sidereal time in radians
        
    Returns
    -------    
    np.ndarray
        3x3 rotation matrix
    """
    hadec = create_topo_to_hadec_matrix(alt, az, lat)
    lst_rot = create_lst_rotation_matrix(lst)
    return combine_rotations(lst_rot, hadec)

def get_topo_to_ecef_matrix(alt: float, az: float, lat: float, lon: float) -> np.ndarray:
    """
    Get the rotation matrix from Topocentric-Horizon to ECEF.
    
    Parameters
    ----------
    alt : float
        Altitude angle in radians
    az : float
        Azimuth angle in radians
    lat : float
        Observer's geodetic latitude in radians
    lon : float
        Observer's longitude in radians
        
    Returns
    -------    
    np.ndarray
        3x3 rotation matrix
    """
    enu = create_topo_to_enu_matrix(alt, az)
    ecef = create_enu_to_ecef_matrix(lat, lon)
    return combine_rotations(ecef, enu)

def topo_to_gcrf(r_topo: np.ndarray, alt: float, az: float, lat: float, lst: float) -> np.ndarray:
    """
    Transform a vector from Topocentric-Horizon to GCRF/ECI.
    
    Parameters
    ----------
    r_topo : np.ndarray
        Position vector in topocentric horizon coordinates (meters)
    alt : float
        Altitude angle in radians
    az : float
        Azimuth angle in radians
    lat : float
        Observer's geodetic latitude in radians
    lst : float
        Local sidereal time in radians
        
    Returns
    -------    
    np.ndarray
        Position vector in GCRF coordinates (meters)
    """
    rotation = get_topo_to_gcrf_matrix(alt, az, lat, lst)
    return rotation @ r_topo

def gcrf_to_topo(r_gcrf: np.ndarray, alt: float, az: float, lat: float, lst: float) -> np.ndarray:
    """
    Transform a vector from GCRF/ECI to Topocentric-Horizon.
    
    Parameters
    ----------
    r_gcrf : np.ndarray
        Position vector in GCRF coordinates (meters)
    alt : float
        Altitude angle in radians
    az : float
        Azimuth angle in radians
    lat : float
        Observer's geodetic latitude in radians
    lst : float
        Local sidereal time in radians
        
    Returns
    -------    
    np.ndarray
        Position vector in topocentric horizon coordinates (meters)
    """
    rotation = get_topo_to_gcrf_matrix(alt, az, lat, lst)
    return invert_rotation(rotation) @ r_gcrf

def topo_to_ecef(r_topo: np.ndarray, alt: float, az: float, lat: float, lon: float) -> np.ndarray:
    """
    Transform a vector from Topocentric-Horizon to ECEF.
    
    Parameters
    ----------
    r_topo : np.ndarray
        Position vector in topocentric horizon coordinates (meters)
    alt : float
        Altitude angle in radians
    az : float
        Azimuth angle in radians
    lat : float
        Observer's geodetic latitude in radians
    lon : float
        Observer's longitude in radians
        
    Returns
    -------    
    np.ndarray
        Position vector in ECEF coordinates (meters)
    """
    rotation = get_topo_to_ecef_matrix(alt, az, lat, lon)
    return rotation @ r_topo

def ecef_to_topo(r_ecef: np.ndarray, alt: float, az: float, lat: float, lon: float) -> np.ndarray:
    """
    Transform a vector from ECEF to Topocentric-Horizon.
    
    Parameters
    ----------
    r_ecef : np.ndarray
        Position vector in ECEF coordinates (meters)
    alt : float
        Altitude angle in radians
    az : float
        Azimuth angle in radians
    lat : float
        Observer's geodetic latitude in radians
    lon : float
        Observer's longitude in radians
        
    Returns
    -------    
    np.ndarray
        Position vector in topocentric horizon coordinates (meters)
    """
    rotation = get_topo_to_ecef_matrix(alt, az, lat, lon)
    return invert_rotation(rotation) @ r_ecef