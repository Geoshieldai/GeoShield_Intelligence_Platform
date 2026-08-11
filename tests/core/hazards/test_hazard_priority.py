from core.hazards.hazard_priority import HazardPriority


def test_hazard_priority():

    priority = HazardPriority()

    result = priority.rank({
        "hazard_results": {
            "Flood": {
                "risk_score": 90,
                "severity": "Extreme",
            },
            "Drought": {
                "risk_score": 50,
                "severity": "Moderate",
            },
        }
    })

    assert result[0]["hazard"] == "Flood"
    assert result[0]["priority"] == 1
    assert result[1]["hazard"] == "Drought"
    assert result[1]["priority"] == 2