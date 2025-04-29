"""
Physical and astronomical constants.
Values are provided in both SI units and kilometer-based units for astrodynamics calculations.
"""

from astropy.constants import G, M_sun, R_sun, L_sun, M_earth, R_earth, M_jup, R_jup, au, c, h, k_B, sigma_sb
from .conversions.units import meters_to_kilometers, cubic_meters_to_cubic_kilometers

# Gravitational constant
GRAVITATIONAL_CONSTANT = G.value  # m^3 / (kg * s^2)

# Solar constants
SOLAR_MASS = M_sun.value  # kg
SOLAR_RADIUS = R_sun.value  # m
SOLAR_LUMINOSITY = L_sun.value  # W

# Gravitational parameter (mu = G * M)
SOLAR_GRAVITATIONAL_PARAMETER = (G * M_sun).value  # m^3 / s^2
SOLAR_GRAVITATIONAL_PARAMETER_KM = cubic_meters_to_cubic_kilometers(SOLAR_GRAVITATIONAL_PARAMETER)  # km^3 / s^2

# Earth constants
EARTH_MASS = M_earth.value  # kg
EARTH_RADIUS = R_earth.value  # m
EARTH_RADIUS_KM = meters_to_kilometers(EARTH_RADIUS)  # km

EARTH_GRAVITATIONAL_PARAMETER = (G * M_earth).value  # m^3 / s^2
EARTH_GRAVITATIONAL_PARAMETER_KM = cubic_meters_to_cubic_kilometers(EARTH_GRAVITATIONAL_PARAMETER)  # km^3 / s^2

# Jupiter constants
JUPITER_MASS = M_jup.value  # kg
JUPITER_RADIUS = R_jup.value  # m
JUPITER_RADIUS_KM = meters_to_kilometers(JUPITER_RADIUS)  # km

JUPITER_GRAVITATIONAL_PARAMETER = (G * M_jup).value  # m^3 / s^2
JUPITER_GRAVITATIONAL_PARAMETER_KM = cubic_meters_to_cubic_kilometers(JUPITER_GRAVITATIONAL_PARAMETER)  # km^3 / s^2

# Astronomical Unit
ASTRONOMICAL_UNIT = au.value  # m
ASTRONOMICAL_UNIT_KM = meters_to_kilometers(ASTRONOMICAL_UNIT)  # km

# Speed of light
SPEED_OF_LIGHT = c.value  # m/s

# Planck constant
PLANCK_CONSTANT = h.value  # J*s

# Boltzmann constant
BOLTZMANN_CONSTANT = k_B.value  # J/K

# Stefan-Boltzmann constant
STEFAN_BOLTZMANN_CONSTANT = sigma_sb.value  # W / (m^2 * K^4)

# Dictionary mapping celestial bodies to their gravitational parameters (m³/s²)
CELESTIAL_BODIES = {
    'earth': EARTH_GRAVITATIONAL_PARAMETER,
    'sun': SOLAR_GRAVITATIONAL_PARAMETER,
    'jupiter': JUPITER_GRAVITATIONAL_PARAMETER
}

# Dictionary mapping celestial bodies to their gravitational parameters (km³/s²)
CELESTIAL_BODIES_KM = {
    'earth': EARTH_GRAVITATIONAL_PARAMETER_KM,
    'sun': SOLAR_GRAVITATIONAL_PARAMETER_KM,
    'jupiter': JUPITER_GRAVITATIONAL_PARAMETER_KM
}