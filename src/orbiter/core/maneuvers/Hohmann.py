"""
ΔV calculators.  First cut: Hohmann transfer between co-axial circular orbits.
"""

import numpy as np
from ..constants.AstroConstants import EARTH_MASS
from ..constants.AstroConstants import GRAVITATIONAL_CONSTANT as G

def hohmann_delta_v(r1: float, r2: float, body_mass: float = EARTH_MASS) -> tuple[float, float, float]:
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
    dv1, dv2, dv_total  (all in m/s)
    """
    if r1 <= 0 or r2 <= 0:
        raise ValueError("Orbit radii must be positive")
    if body_mass <= 0:
        raise ValueError("Body mass must be positive")

    mu = G * body_mass  # Standard gravitational parameter

    # Calculate circular orbital speeds
    v1_circular = np.sqrt(mu / r1)
    v2_circular = np.sqrt(mu / r2)

    # Calculate transfer speeds
    v1_transfer = np.sqrt(mu * (2 / r1 - 1 / (0.5 * (r1 + r2))))
    v2_transfer = np.sqrt(mu * (2 / r2 - 1 / (0.5 * (r1 + r2))))

    # Determine if the orbit is being raised or lowered
    if r2 > r1:
        # Orbit is being raised
        dv1 = v1_transfer - v1_circular
        dv2 = v2_circular - v2_transfer
    else:
        # Orbit is being lowered
        dv1 = v1_transfer + v1_circular
        dv2 = -(v2_transfer + v2_circular)

    return dv1, dv2, abs(dv1) + abs(dv2)
