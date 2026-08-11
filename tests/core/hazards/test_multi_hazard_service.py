from core.hazards.multi_hazard_service import MultiHazardService


def test_multi_hazard_service():

    service = MultiHazardService()

    result = service.analyze({
        "hazards": [
            "Drought",
            "Vegetation Degradation",
        ],
        "hazard_results": {
            "Drought": {
                "risk_score": 80,
                "severity": "Extreme",
            },
            "Vegetation Degradation": {
                "risk_score": 70,
                "severity": "High",
            },
        },
    })

    assert "multi_hazard" in result
    assert "priority" in result
    assert "summary" in result

    assert result["priority"][0]["hazard"] == "Drought"