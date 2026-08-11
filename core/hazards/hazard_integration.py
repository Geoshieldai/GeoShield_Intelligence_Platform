"""
GeoShield Hazard Integration.

Connects environmental intelligence outputs
to the hazard intelligence service.
"""

from core.hazards.hazard_service import HazardService


class HazardIntegration:
    """
    Integrates environmental analysis with hazard analysis.
    """

    def __init__(self):
        self.service = HazardService()

    def process(
        self,
        environmental_result: dict,
    ) -> dict:
        """
        Process an environmental intelligence result.
        """

        indices = environmental_result.get(
            "indices",
            {},
        )

        environmental_score = environmental_result.get(
            "environmental_score",
            0.0,
        )

        return self.service.analyze(
            ndvi=float(indices.get("ndvi", 0.0)),
            ndwi=float(indices.get("ndwi", 0.0)),
            ndbi=float(indices.get("ndbi", 0.0)),
            savi=float(indices.get("savi", 0.0)),
            environmental_score=float(
                environmental_score
            ),
        )