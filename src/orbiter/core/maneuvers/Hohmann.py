"""
ΔV calculators.  First cut: Hohmann transfer between co-axial circular orbits.
"""

import numpy as np
from ..constants.AstroConstants import EARTH_MASS
from ..constants.AstroConstants import GRAVITATIONAL_CONSTANT as G

def hohmann_delta_v(r1: float, r2: float, body_mass: float = EARTH_MASS) -> tuple[float, float, float, float]:
    """
    Parameters
    ----------
    r1 : float
        Initial circular-orbit radius (m).
    r2 : float
        Final circular-orbit radius (m).
    body_mass : float, optional
        Mass of the central body being orbited (kg). Default is Earth's mass.

    Returns
    -------
    tuple[float, float, float, float]: (dv1, dv2, dv_total, a_transfer)
        dv1: First burn delta-v (m/s)
        dv2: Second burn delta-v (m/s)
        dv_total: Total delta-v (m/s)
        a_transfer: Transfer orbit semi-major axis (m)
    """
    if r1 <= 0 or r2 <= 0:
        raise ValueError("Orbit radii must be positive")
    if body_mass <= 0:
        raise ValueError("Body mass must be positive")

    mu = G * body_mass  # Standard gravitational parameter

    # Calculate transfer orbit energy
    E_transfer = -mu / (r1 + r2)  # Energy of the transfer orbit

    # Calculate the semi-major axis of the transfer orbit
    a_transfer = (r1 + r2) / 2

    # Calculate the semi-latus rectum of the transfer orbit
    p_transfer = 2 * a_transfer * (1 - (r1 * r2) / (a_transfer * (r1 + r2)))


    # Calculate circular orbital speeds
    v1_circular = np.sqrt(mu / r1)
    v2_circular = np.sqrt(mu / r2)

    # Calculate transfer speeds
    v1_transfer = np.sqrt(2 * ((mu / r1) + E_transfer))
    v2_transfer = np.sqrt(2 * ((mu / r2) + E_transfer))

    # Determine if the orbit is being raised or lowered
    if r2 > r1:
        # Orbit is being raised
        dv1 = v1_transfer - v1_circular
        dv2 = v2_circular - v2_transfer
    else:
        # Orbit is being lowered
        dv1 = v1_transfer + v1_circular
        dv2 = v2_transfer + v2_circular

    # total delta-v is the sum of the two impulses
    dv_total = dv1 + dv2

    # Calculate the Time of flight for the transfer orbit
    t_transfer = np.pi * np.sqrt((a_transfer**3) / mu)  # Half-period of the transfer orbit
    return dv1, dv2, dv_total, a_transfer, p_transfer,t_transfer
