"""
ΔV calculators.  First cut: Hohmann transfer between co-axial circular orbits.
"""

import numpy as np
from .states import MU_EARTH

def hohmann_delta_v(r1: float, r2: float) -> tuple[float, float, float]:
    """
    Parameters
    ----------
    r1 : float
        Initial circular-orbit radius (m).
    r2 : float
        Final circular-orbit radius (m).

    Returns
    -------
    dv1, dv2, dv_total  (all in m/s)
    """
    if r1 <= 0 or r2 <= 0:
        raise ValueError("Orbit radii must be positive")

    a_trans = 0.5 * (r1 + r2)
    dv1 = np.sqrt(MU_EARTH / r1) * (np.sqrt(2 * r2 / (r1 + r2)) - 1)
    dv2 = np.sqrt(MU_EARTH / r2) * (1 - np.sqrt(2 * r1 / (r1 + r2)))
    return dv1, dv2, abs(dv1) + abs(dv2)
