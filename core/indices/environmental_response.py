"""
GeoShield Environmental Response Builder

Converts EnvironmentalService results into a consistent
application response.
"""


def build_environmental_response(result: dict) -> dict:
    """
    Build a standardized GeoShield environmental response.
    """

    return {
        "status": "success",
        "environmental_score": result["environmental_score"],
        "condition": result["report"]["condition"],
        "risk_level": result["report"]["risk_level"],
        "classifications": result["classifications"],
        "indices": result["indices"],
        "report": result["report"],
    }