from core.hazards.hazard_service import HazardService


def test_hazard_service():

    service = HazardService()

    result = service.analyze(
        ndvi=0.1,
        ndwi=0.1,
        ndbi=0.1,
        savi=0.1,
        environmental_score=20,
    )

    assert "analysis" in result
    assert "report" in result
    assert "response" in result

    assert "Drought" in result["analysis"]["hazards"]