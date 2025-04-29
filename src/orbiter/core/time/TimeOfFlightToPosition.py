"""
Time of flight calculations for orbital mechanics using SI units (meters, seconds).
"""

import numpy as np
from ..constants.AstroConstants import (
    EARTH_GRAVITATIONAL_PARAMETER,
    SOLAR_GRAVITATIONAL_PARAMETER,
    JUPITER_GRAVITATIONAL_PARAMETER
)
from ..propagation.TheKeplerProblem import stumpff_C, stumpff_S

# Dictionary mapping celestial bodies to their gravitational parameters (m³/s²)
CELESTIAL_BODIES = {
    'earth': EARTH_GRAVITATIONAL_PARAMETER,
    'sun': SOLAR_GRAVITATIONAL_PARAMETER,
    'jupiter': JUPITER_GRAVITATIONAL_PARAMETER
}

def time_of_flight_to_position(r0: np.ndarray, v0: np.ndarray, rf: np.ndarray, body: str = 'earth', mu: float = None) -> float:
    """
    Compute Δt to go from r0 to rf along orbit defined by (r0,v0).
    Handles elliptical, hyperbolic, parabolic trajectories.
    
    Parameters
    ----------
    r0, v0 : array_like
        Initial state vectors (m, m/s).
    rf : array_like
        Final position vector (m).
    body : str, optional
        Celestial body ('earth', 'sun', 'jupiter'). Default is 'earth'.
    mu : float, optional
        Custom gravitational parameter (m^3/s^2). If provided, overrides the 'body' parameter.

    Returns
    -------
    dt : float
        Time-of-flight in seconds.
    """
    # Determine the gravitational parameter to use
    if mu is None:
        try:
            mu = CELESTIAL_BODIES[body.lower()]
        except KeyError:
            raise ValueError(f"Unknown celestial body '{body}'. Must be one of {list(CELESTIAL_BODIES.keys())} or provide mu directly.")

    r0 = np.array(r0, dtype=float)
    v0 = np.array(v0, dtype=float)
    rf = np.array(rf, dtype=float)
    r0_norm = np.linalg.norm(r0)

    # Specific orbital energy
    energy = np.dot(v0, v0) / 2 - mu / r0_norm
    # Angular momentum vector and magnitude
    h_vec = np.cross(r0, v0)
    h = np.linalg.norm(h_vec)
    # Semilatus rectum
    p = h**2 / mu
    # Eccentricity vector and magnitude
    e_vec = (np.cross(v0, h_vec) / mu) - (r0 / r0_norm)
    e = np.linalg.norm(e_vec)

    def true_anomaly(r):
        cosf = np.dot(e_vec, r) / (e * np.linalg.norm(r))
        f = np.arccos(np.clip(cosf, -1.0, 1.0))
        if np.dot(np.cross(e_vec, r), h_vec) < 0:
            f = 2 * np.pi - f
        return f

    f0 = true_anomaly(r0)
    ff = true_anomaly(rf)

    # Parabolic trajectory (Barker's equation)
    if abs(energy) < 1e-8:
        D0, Df = np.tan(f0 / 2), np.tan(ff / 2)
        dt = 0.5 * np.sqrt(2 * p**3 / mu) * ((Df + Df**3 / 3) - (D0 + D0**3 / 3))
    # Elliptical trajectory
    elif energy < 0:
        a = -mu / (2 * energy)
        E = lambda f: 2 * np.arctan(np.sqrt((1 - e) / (1 + e)) * np.tan(f / 2))
        dt = np.sqrt(a**3 / mu) * ((E(ff) - E(f0)) - e * (np.sin(E(ff)) - np.sin(E(f0))))
        if dt < 0:
            dt += 2 * np.pi * np.sqrt(a**3 / mu)
    # Hyperbolic trajectory
    else:
        a = -mu / (2 * energy)
        F = lambda f: 2 * np.arctanh(np.sqrt((e - 1) / (e + 1)) * np.tan(f / 2))
        dt = np.sqrt((-a)**3 / mu) * (e * (np.sinh(F(ff)) - np.sinh(F(f0))) - (F(ff) - F(f0)))

    return dt


if __name__ == "__main__":

    print("\n--- TOF between positions examples ---")
    r0 = [7_000_000, 0, 0]  # 7000 km in meters
    v0 = [0, 7546.049108166282, 0]  # 7.54605 km/s in m/s
    # Elliptical (~90° travel)
    rf_e = [0, 7_000_000, 0]  # 7000 km in meters
    dt_e = time_of_flight_to_position(r0, v0, rf_e)
    print(f"Elliptical 90°: Δt={dt_e:.3f} s")

    # Hyperbolic (~90° travel)
    r0h = [8_000_000, 0, 0]  # 8000 km in meters
    v0h = [0, 11000, 0]  # 11 km/s in m/s
    h_h = np.linalg.norm(np.cross(r0h, v0h))
    p_h = h_h**2 / CELESTIAL_BODIES['earth']
    rf_h = [0, p_h, 0]
    dt_h = time_of_flight_to_position(r0h, v0h, rf_h)
    print(f"Hyperbolic 90°:   Δt={dt_h:.3f} s")

    # Parabolic (~90° travel)
    r0p = [8_000_000, 0, 0]  # 8000 km in meters
    vesc = np.sqrt(2 * CELESTIAL_BODIES['earth'] / 8_000_000)
    v0p = [0, vesc, 0]
    h_p = np.linalg.norm(np.cross(r0p, v0p))
    p_p = h_p**2 / CELESTIAL_BODIES['earth']
    rf_p = [0, p_p, 0]
    dt_p = time_of_flight_to_position(r0p, v0p, rf_p)
    print(f"Parabolic 90°:    Δt={dt_p:.3f} s")
