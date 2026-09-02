"""
NDVI Calculator

Calculates the Normalized Difference Vegetation Index (NDVI)
from Red and Near-Infrared (NIR) reflectance values.
"""


def calculate_ndvi(red: float, nir: float) -> float:
    """
    Calculate NDVI.

    NDVI = (NIR - Red) / (NIR + Red)

    Args:
        red: Red-band reflectance value.
        nir: Near-infrared reflectance value.

    Returns:
        NDVI value.

    Raises:
        ValueError: If red + nir equals zero.
    """

    denominator = nir + red

    if denominator == 0:
        raise ValueError("Red and NIR values cannot sum to zero.")

    return (nir - red) / denominator