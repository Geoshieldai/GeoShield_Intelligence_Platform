"""
GeoShield Hazard Risk Engine.

Produces a normalized risk score for detected hazards.
"""


class HazardRisk:
    """
    Calculate hazard risk.
    """

    def calculate(
        self,
        hazard: str,
        environmental_score: float,
    ) -> float:
        """
        Calculate hazard risk.

        Environmental score represents general environmental
        condition. Lower environmental health increases risk.

        Returns:
            Risk score between 0 and 100.
        """

        environmental_score = max(
            0.0,
            min(float(environmental_score), 100.0),
        )

        risk = 100.0 - environmental_score

        return round(max(0.0, min(risk, 100.0)), 2)