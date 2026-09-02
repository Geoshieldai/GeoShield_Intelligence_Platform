from core.indices.environmental_engine import EnvironmentalEngine


def test_environmental_engine():

    engine = EnvironmentalEngine()

    result = engine.analyze(
        ndvi=0.6,
        ndbi=0.2,
        ndwi=0.4,
        savi=0.5,
    )

    assert "indices" in result
    assert "classifications" in result
    assert "environmental_score" in result
    assert "report" in result

    assert result["indices"]["ndvi"] == 0.6
    assert result["indices"]["ndbi"] == 0.2
    assert result["indices"]["ndwi"] == 0.4
    assert result["indices"]["savi"] == 0.5

    assert isinstance(result["environmental_score"], float)
    assert 0 <= result["environmental_score"] <= 100