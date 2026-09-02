"""
BSI — Bare Soil Index

Used to identify exposed/bare soil and land degradation.

Formula:
BSI = ((SWIR + RED) - (NIR + BLUE))
      / ((SWIR + RED) + (NIR + BLUE))
"""


def calculate_bsi(
    swir: float,
    red: float,
    nir: float,
    blue: float,
) -> float:

    numerator = (swir + red) - (nir + blue)
    denominator = (swir + red) + (nir + blue)

    if denominator == 0:
        return 0.0

    return numerator / denominator