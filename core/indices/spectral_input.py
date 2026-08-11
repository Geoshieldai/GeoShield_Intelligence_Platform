"""
GeoShield Spectral Input

Represents the satellite-band values required
for spectral analysis.
"""

from dataclasses import dataclass


@dataclass
class SpectralInput:
    red: float
    green: float
    nir: float
    swir: float