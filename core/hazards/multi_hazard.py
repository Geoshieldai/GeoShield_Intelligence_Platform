"""
GeoShield Multi-Hazard Intelligence.

Combines multiple detected hazards into a single
compound-risk assessment.
"""


class MultiHazardAnalyzer:
    """
    Analyze interactions between multiple hazards.
    """

    def analyze(self, hazard_analysis: dict) -> dict:
        hazards = hazard_analysis.get("hazards", [])
        results = hazard_analysis.get("hazard_results", {})

        compound_risks = []

        hazard_set = set(hazards)

        if "Drought" in hazard_set and "Vegetation Degradation" in hazard_set:
            compound_risks.append({
                "hazards": ["Drought", "Vegetation Degradation"],
                "type": "Environmental Stress",
                "description": (
                    "Vegetation deterioration is occurring alongside "
                    "potential drought conditions."
                ),
                "risk_level": "High",
            })

        if "Flood" in hazard_set and "Urban Expansion" in hazard_set:
            compound_risks.append({
                "hazards": ["Flood", "Urban Expansion"],
                "type": "Urban Flood Risk",
                "description": (
                    "High surface-water conditions overlap with "
                    "high built-up intensity."
                ),
                "risk_level": "High",
            })

        if (
            "Flood" in hazard_set
            and "Vegetation Degradation" in hazard_set
        ):
            compound_risks.append({
                "hazards": ["Flood", "Vegetation Degradation"],
                "type": "Environmental Flood Stress",
                "description": (
                    "Flood conditions are occurring alongside "
                    "vegetation degradation."
                ),
                "risk_level": "Moderate",
            })

        if len(hazards) >= 3:
            compound_risks.append({
                "hazards": hazards,
                "type": "Multi-Hazard Event",
                "description": (
                    "Multiple environmental hazards are detected "
                    "within the same analysis."
                ),
                "risk_level": "Extreme",
            })

        return {
            "hazard_count": len(hazards),
            "compound_risks": compound_risks,
            "individual_results": results,
        }