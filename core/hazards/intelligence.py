"""
GeoShield Hazard Intelligence Interface.

Combines the standard hazard service with
multi-hazard intelligence.
"""

from core.hazards.hazard_service import HazardService
from core.hazards.multi_hazard_service import MultiHazardService


class HazardIntelligence:

    def __init__(self):
        self.hazard_service = HazardService()
        self.multi_hazard_service = MultiHazardService()

    def analyze(
        self,
        ndvi: float,
        ndwi: float,
        ndbi: float,
        savi: float,
        environmental_score: float,
    ) -> dict:

        hazard_result = self.hazard_service.analyze(
            ndvi=ndvi,
            ndwi=ndwi,
            ndbi=ndbi,
            savi=savi,
            environmental_score=environmental_score,
        )

        multi_hazard_result = (
            self.multi_hazard_service.analyze(
                hazard_result["analysis"]
            )
        )

        return {
            "hazard": hazard_result,
            "multi_hazard": multi_hazard_result,
        }