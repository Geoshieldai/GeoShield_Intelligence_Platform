"""
GeoShield Hazard Response Engine.

Produces recommended response actions based on
detected hazard severity.
"""


def generate_hazard_response(
    hazard_analysis: dict,
) -> list[str]:
    """
    Generate recommended response actions.
    """

    actions = []

    results = hazard_analysis.get(
        "hazard_results",
        {},
    )

    for hazard, result in results.items():

        severity = result.get(
            "severity",
            "Minimal",
        )

        if severity == "Extreme":

            actions.append(
                f"Immediate emergency response required for {hazard}."
            )

            actions.append(
                f"Notify relevant disaster-management authorities about {hazard}."
            )

            actions.append(
                f"Deploy field monitoring and prepare emergency resources for {hazard}."
            )

        elif severity == "High":

            actions.append(
                f"Increase monitoring for {hazard}."
            )

            actions.append(
                f"Notify relevant response authorities about elevated {hazard} risk."
            )

        elif severity == "Moderate":

            actions.append(
                f"Continue monitoring {hazard} conditions."
            )

        elif severity == "Low":

            actions.append(
                f"Maintain routine monitoring of {hazard} conditions."
            )

        else:

            actions.append(
                f"No immediate intervention required for {hazard}."
            )

    if not actions:
        actions.append(
            "No immediate hazard response action required."
        )

    return actions