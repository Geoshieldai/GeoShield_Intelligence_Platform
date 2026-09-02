"""
NDBI Calculator

Calculates the Normalized Difference Built-up Index (NDBI).
"""


def calculate_ndbi(swir: float, nir: float) -> float:
    """
    Calculate NDBI.

    NDBI = (SWIR - NIR) / (SWIR + NIR)

    Args:
        swir: Short-wave infrared reflectance value.
        nir: Near-infrared reflectance value.

    Returns:
        NDBI value.

    Raises:
        ValueError: If SWIR + NIR equals zero.
    """

    denominator = swir + nir

    if denominator == 0:
        raise ValueError("SWIR and NIR values cannot sum to zero.")

    return (swir - nir) / denominator