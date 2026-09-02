"""
GeoShield Spectral Report

Stores the calculated spectral intelligence
for a satellite observation.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class SpectralReport:
    values: Dict[str, float]
    classifications: Dict[str, str]