"""
GeoShield Environmental Integration Test

Verifies that environmental indices can flow through
the EnvironmentalEngine as one integrated analysis.
"""

from core.indices.environmental_engine import EnvironmentalEngine


def test_environmental_integration():

    engine = EnvironmentalEngine()

    result = engine.analyze(
        ndvi=0.65,
        ndbi=0.10,
        ndwi=0.30,
        savi=0.55,
        evi=0.50,
    )

    assert isinstance(result, dict)

    assert "indices" in result
    assert "classifications" in result
    assert "environmental_score" in result
    assert "report" in result

    assert result["indices"]["ndvi"] == 0.65
    assert result["indices"]["ndbi"] == 0.10
    assert result["indices"]["ndwi"] == 0.30
    assert result["indices"]["savi"] == 0.55
    assert result["indices"]["evi"] == 0.50

    assert isinstance(
        result["environmental_score"],
        float,
    )

    assert 0 <= result["environmental_score"] <= 100