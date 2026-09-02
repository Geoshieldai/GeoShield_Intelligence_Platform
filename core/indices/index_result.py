"""
Spectral Index Result

Standard result object used by GeoShield's index classifiers.
"""

from dataclasses import dataclass


@dataclass
class IndexResult:
    index: str
    value: float
    classification: str
    confidence: float = 1.0