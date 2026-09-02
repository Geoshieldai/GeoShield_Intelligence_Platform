from core.indices.environmental_service import EnvironmentalService


def test_environmental_service():

    service = EnvironmentalService()

    result = service.analyze(
        ndvi=0.6,
        ndbi=0.1,
        ndwi=0.3,
        savi=0.5,
    )

    assert "indices" in result
    assert "classifications" in result
    assert "environmental_score" in result
    assert "report" in result

    assert result["indices"]["ndvi"] == 0.6
    assert result["indices"]["ndbi"] == 0.1
    assert result["indices"]["ndwi"] == 0.3
    assert result["indices"]["savi"] == 0.5

    assert 0 <= result["environmental_score"] <= 100