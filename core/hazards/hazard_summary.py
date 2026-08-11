"""
GeoShield Hazard Summary.

Creates a concise summary from multi-hazard analysis.
"""


def generate_hazard_summary(
    hazard_analysis: dict,
    multi_hazard_analysis: dict,
    priority_results: list[dict],
) -> dict:

    hazards = hazard_analysis.get(
        "hazards",
        [],
    )

    compound_risks = multi_hazard_analysis.get(
        "compound_risks",
        [],
    )

    if priority_results:
        highest_priority = priority_results[0]
    else:
        highest_priority = None

    return {
        "hazard_count": len(hazards),
        "compound_risk_count": len(compound_risks),
        "highest_priority_hazard": highest_priority,
        "status": (
            "Hazards Detected"
            if hazards
            else "No Significant Hazard Detected"
        ),
    }