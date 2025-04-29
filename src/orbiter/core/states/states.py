"""
Lightweight conversions between Cartesian state-vectors and
classical orbital elements (COE).   SI units only (metre, second, radian).
"""

from dataclasses import dataclass
import numpy as np
import astropy.units as u
from astropy.coordinates import CartesianRepresentation

MU_EARTH = 3.986_004_418e14  # m³ s⁻²  (WGS-84)

@dataclass
class StateRV:
    r: np.ndarray  # shape (3,), metres
    v: np.ndarray  # shape (3,), metres / second

    def as_coe(self) -> "ClassicalOE":
        r_vec, v_vec = self.r, self.v
        r_norm = np.linalg.norm(r_vec)
        h_vec = np.cross(r_vec, v_vec)
        h_norm = np.linalg.norm(h_vec)
        i = np.arccos(h_vec[2] / h_norm)

        n_vec = np.cross([0, 0, 1], h_vec)
        n_norm = np.linalg.norm(n_vec)
        raan = np.arctan2(n_vec[1], n_vec[0]) % (2 * np.pi)

        e_vec = (np.cross(v_vec, h_vec) / MU_EARTH) - (r_vec / r_norm)
        e = np.linalg.norm(e_vec)
        argp = (
            np.arccos(np.dot(n_vec, e_vec) / (n_norm * e))
            if e != 0 else 0.0
        )
        if e_vec[2] < 0:
            argp = 2 * np.pi - argp

        nu = np.arccos(np.dot(e_vec, r_vec) / (e * r_norm))
        if np.dot(r_vec, v_vec) < 0:
            nu = 2 * np.pi - nu

        a = 1 / ((2 / r_norm) - (np.linalg.norm(v_vec) ** 2) / MU_EARTH)

        return ClassicalOE(a, e, i, raan, argp, nu)

@dataclass
class ClassicalOE:
    a: float      # semi-major axis (m)
    e: float      # eccentricity
    i: float      # inclination (rad)
    raan: float   # right ascension of asc. node (rad)
    argp: float   # argument of perigee (rad)
    nu: float     # true anomaly (rad)

    def as_rv(self) -> StateRV:
        # (two-body, no perturbations)
        p = self.a * (1 - self.e ** 2)
        r_pqw = np.array([
            p * np.cos(self.nu) / (1 + self.e * np.cos(self.nu)),
            p * np.sin(self.nu) / (1 + self.e * np.cos(self.nu)),
            0.0,
        ])

        v_pqw = np.array([
            -np.sqrt(MU_EARTH / p) * np.sin(self.nu),
            np.sqrt(MU_EARTH / p) * (self.e + np.cos(self.nu)),
            0.0,
        ])

        # rotation matrix PQW→IJK
        cos_O, sin_O = np.cos(self.raan), np.sin(self.raan)
        cos_i, sin_i = np.cos(self.i), np.sin(self.i)
        cos_w, sin_w = np.cos(self.argp), np.sin(self.argp)

        R = np.array([
            [cos_O * cos_w - sin_O * sin_w * cos_i,
             -cos_O * sin_w - sin_O * cos_w * cos_i,
             sin_O * sin_i],
            [sin_O * cos_w + cos_O * sin_w * cos_i,
             -sin_O * sin_w + cos_O * cos_w * cos_i,
             -cos_O * sin_i],
            [sin_w * sin_i,
             cos_w * sin_i,
             cos_i]
        ])

        r_ijk = R @ r_pqw
        v_ijk = R @ v_pqw
        return StateRV(r_ijk, v_ijk)
