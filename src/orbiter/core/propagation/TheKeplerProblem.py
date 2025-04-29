"""
Universal variable formulation of Kepler's problem for orbit propagation.
All calculations in kilometer-based units.
"""

import numpy as np
from ..constants.AstroConstants import CELESTIAL_BODIES_KM

def stumpff_C(z):
    """
    Stumpff function C(z) = (1 - cos(sqrt(z))) / z for z > 0,
    and (1 - cosh(sqrt(-z))) / z for z < 0, with series expansion at z=0.
    """
    if np.isclose(z, 0.0):
        return 1.0 / 2.0
    elif z > 0:
        return (1 - np.cos(np.sqrt(z))) / z
    else:
        return (1 - np.cosh(np.sqrt(-z))) / z


def stumpff_S(z):
    """
    Stumpff function S(z) = (sqrt(z) - sin(sqrt(z))) / (z**1.5) for z > 0,
    and (sinh(sqrt(-z)) - sqrt(-z)) / ((-z)**1.5) for z < 0, with series expansion at z=0.
    """
    if np.isclose(z, 0.0):
        return 1.0 / 6.0
    elif z > 0:
        return (np.sqrt(z) - np.sin(np.sqrt(z))) / (z * np.sqrt(z))
    else:
        return (np.sinh(np.sqrt(-z)) - np.sqrt(-z)) / ((-z) * np.sqrt(-z))


def universal_kepler(r0, v0, dt, body='earth', mu=None, tol=1e-8, max_iter=1000):
    """
    Propagate position and velocity vectors (r0, v0) forward by dt seconds
    under a Keplerian two-body field (universal variable formulation).

    Parameters
    ----------
    r0 : array_like
        Initial position vector in km.
    v0 : array_like
        Initial velocity vector in km/s.
    dt : float
        Time of flight in seconds.
    body : str, optional
        Celestial body for the propagation ('earth', 'sun', 'jupiter').
        Default is 'earth'.
    mu : float, optional
        Custom gravitational parameter (km^3/s^2). If provided, overrides the 'body' parameter.
    tol : float, optional
        Convergence tolerance on universal anomaly.
    max_iter : int, optional
        Max number of Newton iterations.

    Returns
    -------
    r : ndarray
        Propagated position vector in km.
    v : ndarray
        Propagated velocity vector in km/s.

    Raises
    ------
    ValueError
        If body is not recognized and mu is not provided.
    RuntimeError
        If Newton iteration does not converge.
    """
    # Determine the gravitational parameter to use
    if mu is None:
        try:
            mu = CELESTIAL_BODIES_KM[body.lower()]
        except KeyError:
            raise ValueError(f"Unknown celestial body '{body}'. Must be one of {list(CELESTIAL_BODIES_KM.keys())} or provide mu directly.")
    
    r0 = np.array(r0, dtype=float)
    v0 = np.array(v0, dtype=float)
    r0_norm = np.linalg.norm(r0)
    vr0 = np.dot(r0, v0) / r0_norm
    alpha = 2.0 / r0_norm - np.dot(v0, v0) / mu

    # Initial guess for universal anomaly x
    if alpha > 0:
        x = np.sqrt(mu) * dt * alpha
    else:
        x = np.sign(dt) * np.sqrt(-1 / alpha) * np.log(
            (-2 * mu * alpha * dt) / 
            (vr0 + np.sign(dt) * np.sqrt(-mu / alpha) * (1 - r0_norm * alpha))
        )

    # Newton iteration to solve for x
    ratio = 1
    it = 0
    while abs(ratio) > tol and it < max_iter:
        it += 1
        z = alpha * x**2
        C = stumpff_C(z)
        S = stumpff_S(z)
        F = (r0_norm * vr0 / np.sqrt(mu)) * x**2 * C + (1 - alpha * r0_norm) * x**3 * S + r0_norm * x - np.sqrt(mu) * dt
        dFdx = (r0_norm * vr0 / np.sqrt(mu)) * x * (1 - alpha * x**2 * S) + (1 - alpha * r0_norm) * x**2 * C + r0_norm
        ratio = F / dFdx
        x -= ratio

    if it >= max_iter:
        raise RuntimeError(f"Newton iteration did not converge after {max_iter} iterations")

    # Compute f and g functions
    z = alpha * x**2
    f = 1 - x**2 * C / r0_norm
    g = dt - 1 / np.sqrt(mu) * x**3 * S

    r = f * r0 + g * v0
    r_norm = np.linalg.norm(r)

    # Compute derivatives of f and g
    fdot = np.sqrt(mu) / (r0_norm * r_norm) * x * (z * S - 1)
    gdot = 1 - x**2 * C / r_norm

    v = fdot * r0 + gdot * v0
    return r, v


if __name__ == "__main__":
    # Example: propagate a 7000 km circular LEO by 1 hour
    r0 = [7000.0, 0.0, 0.0]       # km
    v0 = [0.0, 7.546049108166282, 0.0]  # km/s
    dt = 3600.0                   # seconds

    # Using Earth's gravitational parameter from constants
    r, v = universal_kepler(r0, v0, dt, body='earth')
    print(f"Propagated position (km): {r}")
    print(f"Propagated velocity (km/s): {v}")

    # Same propagation but around Jupiter
    r, v = universal_kepler(r0, v0, dt, body='jupiter')
    print(f"\nAround Jupiter:")
    print(f"Propagated position (km): {r}")
    print(f"Propagated velocity (km/s): {v}")
