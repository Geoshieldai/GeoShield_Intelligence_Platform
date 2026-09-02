"""
EVI — Enhanced Vegetation Index

Improves vegetation monitoring in areas where NDVI can be affected
by atmospheric conditions or soil/background effects.

Formula:
EVI = G * (NIR - RED) / (NIR + C1*RED - C2*BLUE + L)

Standard constants:
G  = 2.5
C1 = 6.0
C2 = 7.5
L  = 1.0
"""


def calculate_evi(
    red: float,
    nir: float,
    blue: float,
    g: float = 2.5,
    c1: float = 6.0,
    c2: float = 7.5,
    l: float = 1.0,
) -> float:

    denominator = nir + c1 * red - c2 * blue + l

    if denominator == 0:
        return 0.0

    return g * (nir - red) / denominator