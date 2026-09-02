"""
GeoShield Environmental Analyzer

Connects environmental index processing to the
application-level environmental intelligence workflow.
"""

from core.indices.environmental_service import EnvironmentalService
from core.indices.environmental_response import build_environmental_response


class EnvironmentalAnalyzer:
    """Application-level environmental intelligence analyzer."""

    def __init__(self):
        self.service = EnvironmentalService()

    def analyze(
        self,
        ndvi: float,
        ndbi: float,
        ndwi: float,
        savi: float,
        evi: float | None = None,
    ) -> dict:
        """
        Analyze environmental conditions and return
        a standardized GeoShield response.
        """

        result = self.service.analyze(
            ndvi=ndvi,
            ndbi=ndbi,
            ndwi=ndwi,
            savi=savi,
            evi=evi,
        )

        return build_environmental_response(result)