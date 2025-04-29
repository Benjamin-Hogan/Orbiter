import numpy as np

def plane_change_delta_v(v: float, delta_i: float) -> float:
    """
    Calculate the delta-v required for a simple plane change maneuver.

    Parameters
    ----------
    v : float
        Orbital velocity (m/s). Assuming in circular orbit. Use circular velocity
        formula: v = sqrt(GM/r)
    delta_i : float
        Change in inclination (radians).

    Returns
    -------
    float
        Delta-v required for the plane change (m/s).
    """
    if v <= 0:
        raise ValueError("Orbital velocity must be positive")
    if delta_i < 0 or delta_i > 2 * np.pi:
        raise ValueError("Inclination change must be between 0 and 2π radians")

    # Delta-v for plane change
    delta_v = 2 * v * np.sin(delta_i / 2)
    return delta_v