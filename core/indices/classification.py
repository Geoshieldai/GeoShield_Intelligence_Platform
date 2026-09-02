"""
GeoShield Environmental Classification

Converts environmental index values and scores
into human-readable environmental conditions.
"""


def classify_ndvi(ndvi: float) -> str:
    """Classify vegetation condition using NDVI."""

    if ndvi >= 0.6:
        return "Very Healthy Vegetation"

    if ndvi >= 0.3:
        return "Healthy Vegetation"

    if ndvi >= 0.1:
        return "Sparse Vegetation"

    if ndvi >= 0:
        return "Very Sparse Vegetation"

    return "No Vegetation"


def classify_ndbi(ndbi: float) -> str:
    """Classify built-up intensity using NDBI."""

    if ndbi >= 0.4:
        return "Very High Built-up Area"

    if ndbi >= 0.2:
        return "High Built-up Area"

    if ndbi >= 0:
        return "Moderate Built-up Area"

    return "Low Built-up Area"


def classify_ndwi(ndwi: float) -> str:
    """Classify surface-water condition using NDWI."""

    if ndwi >= 0.5:
        return "High Water Presence"

    if ndwi >= 0.2:
        return "Moderate Water Presence"

    if ndwi >= 0:
        return "Low Water Presence"

    return "Very Low Water Presence"


def classify_savi(savi: float) -> str:
    """Classify vegetation condition using SAVI."""

    if savi >= 0.6:
        return "Very Dense Vegetation"

    if savi >= 0.3:
        return "Dense Vegetation"

    if savi >= 0.1:
        return "Moderate Vegetation"

    if savi >= 0:
        return "Sparse Vegetation"

    return "Very Sparse Vegetation"


def classify_environment(
    ndvi: float,
    ndbi: float,
    ndwi: float,
    savi: float,
) -> dict:
    """Classify all environmental indices."""

    return {
        "ndvi": classify_ndvi(ndvi),
        "ndbi": classify_ndbi(ndbi),
        "ndwi": classify_ndwi(ndwi),
        "savi": classify_savi(savi),
    }


def classify_environmental_condition(score: float) -> str:
    """
    Convert the environmental score into
    a general environmental condition.
    """

    if score >= 80:
        return "Excellent Environmental Condition"

    if score >= 60:
        return "Good Environmental Condition"

    if score >= 40:
        return "Moderate Environmental Condition"

    if score >= 20:
        return "Poor Environmental Condition"

    return "Critical Environmental Condition"


def classify_risk_level(score: float) -> str:
    """
    Convert the environmental score into
    a general environmental risk level.

    Higher environmental health score means lower risk.
    """

    if score >= 80:
        return "Low Risk"

    if score >= 60:
        return "Moderate Risk"

    if score >= 40:
        return "Elevated Risk"

    if score >= 20:
        return "High Risk"

    return "Extreme Risk"