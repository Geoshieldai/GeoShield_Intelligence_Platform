"""
GeoShield Environmental Score

Produces a 0-100 environmental condition score.

Higher score = generally healthier environmental conditions.

EVI is currently included as an additional vegetation-health
signal. The weighting is intentionally simple and will be
calibrated later using real-world datasets.
"""


def _clamp(
    value: float,
    minimum: float = 0.0,
    maximum: float = 100.0,
) -> float:
    """Keep a value within the specified range."""

    return max(minimum, min(value, maximum))


def _normalize_index(value: float) -> float:
    """
    Convert an index approximately in the [-1, 1] range
    into a 0-100 score.
    """

    return _clamp(((value + 1.0) / 2.0) * 100.0)


def calculate_environmental_score(
    ndvi: float,
    ndbi: float,
    ndwi: float,
    savi: float,
    evi: float | None = None,
) -> float:
    """
    Calculate an environmental condition score.

    Components:
    - NDVI: vegetation health
    - SAVI: soil-adjusted vegetation health
    - EVI: enhanced vegetation health
    - NDWI: water presence
    - NDBI: built-up pressure

    EVI is optional so the engine remains compatible with
    earlier analyses that do not provide EVI.
    """

    vegetation_score = _normalize_index(ndvi)

    savi_score = _normalize_index(savi)

    water_score = _normalize_index(ndwi)

    built_up_pressure = _normalize_index(ndbi)
    built_up_score = 100.0 - built_up_pressure

    if evi is not None:
        evi_score = _normalize_index(evi)

        score = (
            vegetation_score * 0.30
            + savi_score * 0.20
            + evi_score * 0.15
            + water_score * 0.20
            + built_up_score * 0.15
        )
    else:
        score = (
            vegetation_score * 0.35
            + savi_score * 0.25
            + water_score * 0.20
            + built_up_score * 0.20
        )

    return round(_clamp(score), 2)