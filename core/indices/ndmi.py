"""
NDMI — Normalized Difference Moisture Index

Measures vegetation/water moisture content.

Formula:
NDMI = (NIR - SWIR) / (NIR + SWIR)
"""


def calculate_ndmi(nir: float, swir: float) -> float:
    denominator = nir + swir

    if denominator == 0:
        return 0.0

    return (nir - swir) / denominator