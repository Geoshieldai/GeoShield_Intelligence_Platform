"""
GeoShield Spectral Analysis Engine

Calculates and classifies multiple spectral
indices from one satellite observation.
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

from .spectral_input import SpectralInput
from .spectral_report import SpectralReport


class SpectralEngine:

    def analyze(self, data: SpectralInput) -> SpectralReport:
        """
        Calculate and classify all supported indices.
        """

        ndvi = calculate_ndvi(
            data.red,
            data.nir,
        )

        ndwi = calculate_ndwi(
            data.green,
            data.nir,
        )

        ndbi = calculate_ndbi(
            data.swir,
            data.nir,
        )

        savi = calculate_savi(
            data.red,
            data.nir,
        )

        return SpectralReport(
            values={
                "NDVI": ndvi,
                "NDWI": ndwi,
                "NDBI": ndbi,
                "SAVI": savi,
            },
            classifications={
                "NDVI": classify_ndvi(ndvi).classification,
                "NDWI": classify_ndwi(ndwi).classification,
                "NDBI": classify_ndbi(ndbi).classification,
                "SAVI": classify_savi(savi).classification,
            },
        )