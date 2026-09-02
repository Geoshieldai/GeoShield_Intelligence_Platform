"""
GeoShield Multi-Hazard Service.

Combines hazard analysis, compound-risk analysis,
priority ranking, and summary generation.
"""

from core.hazards.multi_hazard import MultiHazardAnalyzer
from core.hazards.hazard_priority import HazardPriority
from core.hazards.hazard_summary import generate_hazard_summary


class MultiHazardService:

    def __init__(self):
        self.multi_hazard = MultiHazardAnalyzer()
        self.priority = HazardPriority()

    def analyze(self, hazard_analysis: dict) -> dict:

        multi_hazard_result = self.multi_hazard.analyze(
            hazard_analysis
        )

        priority_results = self.priority.rank(
            hazard_analysis
        )

        summary = generate_hazard_summary(
            hazard_analysis=hazard_analysis,
            multi_hazard_analysis=multi_hazard_result,
            priority_results=priority_results,
        )

        return {
            "multi_hazard": multi_hazard_result,
            "priority": priority_results,
            "summary": summary,
        }