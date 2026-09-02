"""
GeoShield Environmental Intelligence Service

Application-facing service for environmental analysis.

This layer keeps the core EnvironmentalEngine separate from
future APIs, dashboards, satellite ingestion pipelines,
and AI decision systems.
"""

from core.indices.environmental_engine import EnvironmentalEngine


class EnvironmentalService:
    """Service layer for GeoShield environmental intelligence."""

    def __init__(self):
        self.engine = EnvironmentalEngine()

    def analyze(
        self,
        ndvi: float,
        ndbi: float,
        ndwi: float,
        savi: float,
        evi: float | None = None,
    ) -> dict:
        """
        Analyze environmental conditions.

        Returns:
            Structured environmental intelligence result.
        """

        return self.engine.analyze(
            ndvi=ndvi,
            ndbi=ndbi,
            ndwi=ndwi,
            savi=savi,
            evi=evi,
        )