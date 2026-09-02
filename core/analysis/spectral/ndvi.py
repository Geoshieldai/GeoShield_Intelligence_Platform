"""
GeoShield NDVI Analysis Engine

Calculates the Normalized Difference Vegetation Index (NDVI)
from Red and Near-Infrared (NIR) satellite bands.
"""

from __future__ import annotations

import numpy as np


class NDVIAnalyzer:
    """
    Calculates NDVI from Red and NIR raster bands.

    NDVI = (NIR - Red) / (NIR + Red)
    """

    def calculate(
        self,
        red_band: np.ndarray,
        nir_band: np.ndarray,
    ) -> np.ndarray:
        """
        Calculate NDVI.

        Parameters
        ----------
        red_band:
            Red reflectance band.

        nir_band:
            Near-infrared reflectance band.

        Returns
        -------
        numpy.ndarray
            NDVI raster.

        Raises
        ------
        ValueError
            If the input bands have different shapes.
        """

        if red_band.shape != nir_band.shape:
            raise ValueError(
                "Red and NIR bands must have the same shape."
            )

        red = red_band.astype(np.float32)
        nir = nir_band.astype(np.float32)

        denominator = nir + red

        ndvi = np.zeros_like(denominator, dtype=np.float32)

        valid_pixels = denominator != 0

        ndvi[valid_pixels] = (
            (nir[valid_pixels] - red[valid_pixels])
            / denominator[valid_pixels]
        )

        return ndvi