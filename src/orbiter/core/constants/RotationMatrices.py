"""
Fundamental rotation matrices for coordinate frame transformations.
This module serves as the central source of truth for all basic rotation matrices.
"""

import numpy as np

def create_topo_to_enu_matrix(alt: float, az: float) -> np.ndarray:
    """
    Creates rotation matrix from Topocentric Horizon to East-North-Up (ENU)
    
    Parameters
    ----------
    alt : float
        Altitude angle in radians
    az : float
        Azimuth angle in radians
        
    Returns
    -------
    np.ndarray
        3x3 rotation matrix
    """
    sin_alt, cos_alt = np.sin(alt), np.cos(alt)
    sin_az, cos_az = np.sin(az), np.cos(az)
    
    return np.array([
        [-sin_az, -sin_alt * cos_az, cos_alt * cos_az],
        [cos_az, -sin_alt * sin_az, cos_alt * sin_az],
        [0, cos_alt, sin_alt]
    ])

def create_enu_to_ecef_matrix(lat: float, lon: float) -> np.ndarray:
    """
    Creates rotation matrix from East-North-Up (ENU) to Earth-Centered Earth-Fixed (ECEF)
    
    Parameters
    ----------
    lat : float
        Geodetic latitude in radians
    lon : float
        Longitude in radians
        
    Returns
    -------
    np.ndarray
        3x3 rotation matrix
    """
    sin_lat, cos_lat = np.sin(lat), np.cos(lat)
    sin_lon, cos_lon = np.sin(lon), np.cos(lon)
    
    return np.array([
        [-sin_lon, -sin_lat * cos_lon, cos_lat * cos_lon],
        [cos_lon, -sin_lat * sin_lon, cos_lat * sin_lon],
        [0, cos_lat, sin_lat]
    ])

def create_lst_rotation_matrix(lst: float) -> np.ndarray:
    """
    Creates rotation matrix for Local Sidereal Time rotation
    
    Parameters
    ----------
    lst : float
        Local sidereal time in radians
        
    Returns
    -------
    np.ndarray
        3x3 rotation matrix
    """
    sin_lst, cos_lst = np.sin(lst), np.cos(lst)
    
    return np.array([
        [cos_lst, -sin_lst, 0],
        [sin_lst, cos_lst, 0],
        [0, 0, 1]
    ])

def create_topo_to_hadec_matrix(alt: float, az: float, lat: float) -> np.ndarray:
    """
    Creates rotation matrix from Topocentric Horizon to Hour Angle/Declination
    
    Parameters
    ----------
    alt : float
        Altitude angle in radians
    az : float
        Azimuth angle in radians
    lat : float
        Observer's latitude in radians
        
    Returns
    -------
    np.ndarray
        3x3 rotation matrix
    """
    sin_alt, cos_alt = np.sin(alt), np.cos(alt)
    sin_az, cos_az = np.sin(az), np.cos(az)
    sin_lat, cos_lat = np.sin(lat), np.cos(lat)
    
    return np.array([
        [sin_lat * cos_az * cos_alt - sin_alt * cos_lat,
         sin_lat * sin_az * cos_alt,
         sin_alt * sin_lat + cos_lat * cos_az * cos_alt],
        [-sin_az * cos_alt,
         cos_az * cos_alt,
         sin_az * cos_alt],
        [-cos_lat * cos_az * cos_alt + sin_alt * sin_lat,
         -cos_lat * sin_az * cos_alt,
         sin_alt * cos_lat - sin_lat * cos_az * cos_alt]
    ])