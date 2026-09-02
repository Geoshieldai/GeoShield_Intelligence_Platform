"""
GeoShield Spectral Intelligence

Provides spectral indices, classification,
and unified spectral analysis.
"""

from .ndvi import calculate_ndvi
from .ndwi import calculate_ndwi
from .ndbi import calculate_ndbi
from .savi import calculate_savi

from .classifier import (
    classify_ndvi,
    classify_ndwi,
    classify_ndbi,
    classify_savi,
)

from .index_result import IndexResult

from .spectral_input import SpectralInput
from .spectral_report import SpectralReport
from .spectral_engine import SpectralEngine


__all__ = [
    "calculate_ndvi",
    "calculate_ndwi",
    "calculate_ndbi",
    "calculate_savi",
    "classify_ndvi",
    "classify_ndwi",
    "classify_ndbi",
    "classify_savi",
    "IndexResult",
    "SpectralInput",
    "SpectralReport",
    "SpectralEngine",
]