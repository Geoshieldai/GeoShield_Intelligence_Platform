"""
Spectral Index Classifier

Converts raw spectral-index values into
basic GeoShield environmental classifications.
"""

from .index_result import IndexResult
from .thresholds import (
    NDVI_VERY_LOW,
    NDVI_LOW,
    NDVI_MODERATE,
    NDWI_WATER_THRESHOLD,
    NDBI_BUILT_UP_THRESHOLD,
    SAVI_LOW,
    SAVI_MODERATE,
)


def classify_ndvi(value: float) -> IndexResult:
    """
    Classify vegetation condition using NDVI.
    """

    if value < NDVI_VERY_LOW:
        classification = "very_low_vegetation"
    elif value < NDVI_LOW:
        classification = "low_vegetation"
    elif value < NDVI_MODERATE:
        classification = "moderate_vegetation"
    else:
        classification = "high_vegetation"

    return IndexResult(
        index="NDVI",
        value=value,
        classification=classification,
    )


def classify_ndwi(value: float) -> IndexResult:
    """
    Classify water presence using NDWI.
    """

    if value >= NDWI_WATER_THRESHOLD:
        classification = "water_likely"
    else:
        classification = "water_not_detected"

    return IndexResult(
        index="NDWI",
        value=value,
        classification=classification,
    )


def classify_ndbi(value: float) -> IndexResult:
    """
    Classify built-up intensity using NDBI.
    """

    if value >= NDBI_BUILT_UP_THRESHOLD:
        classification = "built_up_likely"
    else:
        classification = "non_built_up"

    return IndexResult(
        index="NDBI",
        value=value,
        classification=classification,
    )


def classify_savi(value: float) -> IndexResult:
    """
    Classify vegetation condition using SAVI.
    """

    if value < SAVI_LOW:
        classification = "low_vegetation"
    elif value < SAVI_MODERATE:
        classification = "moderate_vegetation"
    else:
        classification = "high_vegetation"

    return IndexResult(
        index="SAVI",
        value=value,
        classification=classification,
    )