"""
GeoShield Environmental Intelligence Report

Creates a structured report from environmental indices
and the combined environmental score.
"""

from typing import Optional

from core.indices.classification import (
    classify_environmental_condition,
    classify_risk_level,
)

from core.indices.environmental_score import (
    calculate_environmental_score,
)


def generate_environmental_report(
    ndvi: float,
    ndwi: float,
    ndbi: float,
    savi: float,
    evi: Optional[float] = None,
) -> dict:
    """
    Generate a structured environmental intelligence report.

    NDVI, NDWI, NDBI and SAVI are required because they
    form the baseline environmental score.

    EVI is optional and can be incorporated when available.
    """

    score = calculate_environmental_score(
        ndvi=ndvi,
        ndwi=ndwi,
        ndbi=ndbi,
        savi=savi,
        evi=evi,
    )

    condition = classify_environmental_condition(score)

    risk_level = classify_risk_level(score)

    return {
        "environmental_score": score,
        "condition": condition,
        "risk_level": risk_level,
        "indices": {
            "NDVI": ndvi,
            "NDWI": ndwi,
            "NDBI": ndbi,
            "SAVI": savi,
            "EVI": evi,
        },
    }