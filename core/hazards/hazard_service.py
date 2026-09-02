"""
GeoShield Hazard Intelligence Service.

High-level service that combines hazard analysis,
reporting, and response recommendations.
"""

from core.hazards.hazard_engine import HazardEngine
from core.hazards.hazard_report import generate_hazard_report
from core.hazards.hazard_response import generate_hazard_response


class HazardService:
    """
    High-level hazard intelligence service.
    """

    def __init__(self):
        self.engine = HazardEngine()

    def analyze(
        self,
        ndvi: float,
        ndwi: float,
        ndbi: float,
        savi: float,
        environmental_score: float,
    ) -> dict:
        """
        Perform complete hazard intelligence analysis.
        """

        analysis = self.engine.analyze(
            ndvi=ndvi,
            ndwi=ndwi,
            ndbi=ndbi,
            savi=savi,
            environmental_score=environmental_score,
        )

        report = generate_hazard_report(
            analysis
        )

        response = generate_hazard_response(
            analysis
        )

        return {
            "analysis": analysis,
            "report": report,
            "response": response,
        }