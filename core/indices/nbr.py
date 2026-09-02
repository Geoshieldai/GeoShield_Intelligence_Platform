"""
NBR — Normalized Burn Ratio

Used primarily for burn-scar and wildfire severity analysis.

Formula:
NBR = (NIR - SWIR2) / (NIR + SWIR2)
"""


def calculate_nbr(nir: float, swir2: float) -> float:
    denominator = nir + swir2

    if denominator == 0:
        return 0.0

    return (nir - swir2) / denominator