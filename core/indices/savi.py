"""
SAVI Calculator

Calculates the Soil Adjusted Vegetation Index (SAVI).
"""


def calculate_savi(
    red: float,
    nir: float,
    soil_adjustment: float = 0.5,
) -> float:
    """
    Calculate SAVI.

    SAVI = ((NIR - Red) / (NIR + Red + L)) * (1 + L)

    Args:
        red: Red-band reflectance value.
        nir: Near-infrared reflectance value.
        soil_adjustment: Soil brightness correction factor L.

    Returns:
        SAVI value.

    Raises:
        ValueError: If the denominator equals zero.

    """

    denominator = nir + red + soil_adjustment

    if denominator == 0:
        raise ValueError(
            "NIR + Red + soil adjustment cannot equal zero."
        )

    return (
        ((nir - red) / denominator)
        * (1 + soil_adjustment)
    )