"""
GeoShield Environmental Analysis Engine

Combines environmental indices and produces:

- environmental classifications
- environmental score
- environmental intelligence report
"""

from core.indices.classification import classify_environment
from core.indices.environmental_score import calculate_environmental_score
from core.indices.environmental_report import generate_environmental_report


class EnvironmentalEngine:

    def analyze(
        self,
        ndvi: float,
        ndbi: float,
        ndwi: float,
        savi: float,
        evi: float | None = None,
    ) -> dict:
        """
        Analyze environmental conditions using
        satellite-derived environmental indices.
        """

        classifications = classify_environment(
            ndvi=ndvi,
            ndbi=ndbi,
            ndwi=ndwi,
            savi=savi,
        )

        score = calculate_environmental_score(
            ndvi=ndvi,
            ndbi=ndbi,
            ndwi=ndwi,
            savi=savi,
            evi=evi,
        )

        report = generate_environmental_report(
            ndvi=ndvi,
            ndwi=ndwi,
            ndbi=ndbi,
            savi=savi,
            evi=evi,
        )

        return {
            "indices": {
                "ndvi": ndvi,
                "ndbi": ndbi,
                "ndwi": ndwi,
                "savi": savi,
                "evi": evi,
            },
            "classifications": classifications,
            "environmental_score": score,
            "report": report,
        }