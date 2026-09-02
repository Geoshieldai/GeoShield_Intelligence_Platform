"""
NDWI Calculator

Calculates the Normalized Difference Water Index (NDWI).
"""


def calculate_ndwi(green: float, nir: float) -> float:
    """
    Calculate NDWI.

    NDWI = (Green - NIR) / (Green + NIR)

    Args:
        green: Green-band reflectance value.
        nir: Near-infrared reflectance value.

    Returns:
        NDWI value.

    Raises:
        ValueError: If green + nir equals zero.
    """

    denominator = green + nir

    if denominator == 0:
        raise ValueError("Green and NIR values cannot sum to zero.")

    return (green - nir) / denominator