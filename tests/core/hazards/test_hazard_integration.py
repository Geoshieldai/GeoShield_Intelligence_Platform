from core.hazards.hazard_integration import HazardIntegration


def test_hazard_integration():

    integration = HazardIntegration()

    environmental_result = {
        "indices": {
            "ndvi": 0.1,
            "ndwi": 0.1,
            "ndbi": 0.1,
            "savi": 0.1,
        },
        "environmental_score": 20,
    }

    result = integration.process(
        environmental_result
    )

    assert "analysis" in result
    assert "report" in result
    assert "response" in result

    assert "Drought" in result["analysis"]["hazards"]