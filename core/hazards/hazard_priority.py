"""
GeoShield Hazard Priority Engine.

Ranks hazards according to their risk scores.
"""


class HazardPriority:

    def rank(self, hazard_analysis: dict) -> list[dict]:
        results = hazard_analysis.get(
            "hazard_results",
            {},
        )

        ranked = []

        for hazard, result in results.items():

            ranked.append({
                "hazard": hazard,
                "risk_score": result.get(
                    "risk_score",
                    0.0,
                ),
                "severity": result.get(
                    "severity",
                    "Minimal",
                ),
            })

        ranked.sort(
            key=lambda item: item["risk_score"],
            reverse=True,
        )

        for index, item in enumerate(ranked, start=1):
            item["priority"] = index

        return ranked