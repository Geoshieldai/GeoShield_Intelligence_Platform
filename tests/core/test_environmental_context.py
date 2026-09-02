"""
Tests for GeoShield EnvironmentalContext.
"""

from core.kernel.environmental_context import EnvironmentalContext


def test_environmental_context():

    context = EnvironmentalContext(
        indices={
            "ndvi": 0.6,
            "ndbi": 0.2,
            "ndwi": 0.4,
            "savi": 0.5,
        },
        classifications={
            "ndvi": "Very Healthy Vegetation",
            "ndbi": "High Built-up Area",
            "ndwi": "Moderate Water Presence",
            "savi": "Dense Vegetation",
        },
        environmental_score=75.0,
        condition="Healthy",
        risk_level="Low",
        report={
            "status": "Environmental analysis complete"
        },
    )

    data = context.to_dict()

    assert data["indices"]["ndvi"] == 0.6
    assert data["environmental_score"] == 75.0
    assert data["condition"] == "Healthy"
    assert data["risk_level"] == "Low"