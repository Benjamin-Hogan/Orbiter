"""
Two-body propagation via a simple RK4 integrator.
"""

import numpy as np
from .states import StateRV, MU_EARTH

def propagate_two_body(
    state: StateRV,
    duration: float,
    dt: float
) -> list[StateRV]:
    """
    Propagate under central gravity only.

    Parameters
    ----------
    state : StateRV
        Initial state (r in metres, v in m/s).
    duration : float
        Total propagation time in seconds.
    dt : float
        Time-step in seconds.

    Returns
    -------
    traj : list of StateRV
        State at t = 0, dt, 2·dt, … up to duration.
    """
    def accel(r: np.ndarray) -> np.ndarray:
        return -MU_EARTH * r / np.linalg.norm(r)**3

    steps = max(1, int(np.ceil(duration / dt)))
    traj: list[StateRV] = []
    r = state.r.copy()
    v = state.v.copy()

    for _ in range(steps + 1):
        traj.append(StateRV(r.copy(), v.copy()))

        # RK4 integration
        k1_v = accel(r) * dt
        k1_r = v * dt

        k2_v = accel(r + 0.5 * k1_r) * dt
        k2_r = (v + 0.5 * k1_v) * dt

        k3_v = accel(r + 0.5 * k2_r) * dt
        k3_r = (v + 0.5 * k2_v) * dt

        k4_v = accel(r + k3_r) * dt
        k4_r = (v + k3_v) * dt

        v = v + (k1_v + 2*k2_v + 2*k3_v + k4_v) / 6
        r = r + (k1_r + 2*k2_r + 2*k3_r + k4_r) / 6

    return traj
