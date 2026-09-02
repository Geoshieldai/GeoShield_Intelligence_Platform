"""
GeoShield Hazard Intelligence Engine.

Combines hazard detection, classification, severity,
and risk assessment into a single analysis pipeline.
"""

from core.hazards.detector import HazardDetector
from core.hazards.classifier import HazardClassifier
from core.hazards.severity import HazardSeverity
from core.hazards.risk import HazardRisk


class HazardEngine:
    """
    Main hazard intelligence engine.
    """

    def __init__(self):
        self.detector = HazardDetector()
        self.classifier = HazardClassifier()
        self.severity = HazardSeverity()
        self.risk = HazardRisk()

    def analyze(
        self,
        ndvi: float,
        ndwi: float,
        ndbi: float,
        savi: float,
        environmental_score: float,
    ) -> dict:
        """
        Analyze environmental conditions for potential hazards.
        """

        hazards = self.detector.detect(
            ndvi=ndvi,
            ndwi=ndwi,
            ndbi=ndbi,
            savi=savi,
        )

        classifications = self.classifier.classify(
            hazards
        )

        hazard_results = {}

        for hazard in hazards:

            risk_score = self.risk.calculate(
                hazard=hazard,
                environmental_score=environmental_score,
            )

            severity = self.severity.calculate(
                hazard=hazard,
                score=risk_score,
            )

            hazard_results[hazard] = {
                "risk_score": risk_score,
                "severity": severity,
                "classification": classifications[hazard],
            }

        return {
            "hazards": hazards,
            "classifications": classifications,
            "hazard_results": hazard_results,
            "environmental_score": environmental_score,
        }