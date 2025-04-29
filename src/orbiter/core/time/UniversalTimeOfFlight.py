"""
Universal variable formulation time-of-flight calculations using SI units (meters, seconds).
"""

import numpy as np
from ..constants.AstroConstants import CELESTIAL_BODIES
from ..propagation.TheKeplerProblem import stumpff_C, stumpff_S

def universal_time_of_flight(chi: float, r0: np.ndarray, v0: np.ndarray, body: str = 'earth', mu: float = None) -> float:
    """
    Battin's universal-variable TOF equation (eq. 5.3-28).

    Parameters
    ----------
    chi : float
        Universal anomaly (m^(1/2)). Generalizes eccentric/hyperbolic anomaly
        across conic sections. Serves as the solver variable in iterative
        schemes to match a target Δt.
    r0, v0 : array_like
        Initial state vectors (m, m/s).
    body : str, optional
        Celestial body ('earth', 'sun', 'jupiter'). Default is 'earth'.
    mu : float, optional
        Custom gravitational parameter (m^3/s^2). If provided, overrides the 'body' parameter.

    Returns
    -------
    dt : float
        Time-of-flight in seconds corresponding to χ.
    """
    # Determine the gravitational parameter to use
    if mu is None:
        try:
            mu = CELESTIAL_BODIES[body.lower()]
        except KeyError:
            raise ValueError(f"Unknown celestial body '{body}'. Must be one of {list(CELESTIAL_BODIES.keys())} or provide mu directly.")

    r0 = np.array(r0, dtype=float)
    v0 = np.array(v0, dtype=float)
    r0_norm = np.linalg.norm(r0)
    vr0 = np.dot(r0, v0) / r0_norm
    alpha = 2.0 / r0_norm - np.dot(v0, v0) / mu

    z = alpha * chi**2
    C = stumpff_C(z)
    S = stumpff_S(z)

    dt = ((r0_norm * vr0) / np.sqrt(mu)) * chi**2 * C \
         + (1.0 - alpha * r0_norm) * chi**3 * S \
         + r0_norm * chi
    return dt
