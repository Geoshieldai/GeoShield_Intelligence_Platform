"""
GeoShield Hazard Intelligence Report.

Creates a structured human-readable hazard report.
"""


def generate_hazard_report(
    hazard_analysis: dict,
) -> dict:
    """
    Generate a structured hazard intelligence report.
    """

    hazards = hazard_analysis.get(
        "hazards",
        [],
    )

    results = hazard_analysis.get(
        "hazard_results",
        {},
    )

    if not hazards:
        overall_status = "No Significant Hazard Detected"
    else:
        severity_order = {
            "Extreme": 5,
            "High": 4,
            "Moderate": 3,
            "Low": 2,
            "Minimal": 1,
        }

        highest_severity = max(
            (
                result["severity"]
                for result in results.values()
            ),
            key=lambda value: severity_order.get(
                value,
                0,
            ),
        )

        overall_status = (
            f"{highest_severity} Hazard Conditions Detected"
        )

    return {
        "overall_status": overall_status,
        "hazard_count": len(hazards),
        "hazards": results,
        "environmental_score": hazard_analysis.get(
            "environmental_score"
        ),
    }