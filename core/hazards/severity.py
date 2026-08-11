"""
GeoShield Hazard Severity Engine.

Determines the severity of detected hazards.
"""


class HazardSeverity:
    """
    Calculate hazard severity.
    """

    def calculate(self, hazard: str, score: float) -> str:
        """
        Convert a numerical hazard score into severity.

        Args:
            hazard: Hazard type.
            score: Numerical hazard score from 0 to 100.

        Returns:
            Severity classification.
        """

        score = max(0.0, min(float(score), 100.0))

        if score >= 80:
            return "Extreme"

        if score >= 60:
            return "High"

        if score >= 40:
            return "Moderate"

        if score >= 20:
            return "Low"

        return "Minimal"