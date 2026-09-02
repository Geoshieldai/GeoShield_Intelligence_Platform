from core.hazards.hazard_summary import generate_hazard_summary


def test_hazard_summary():

    result = generate_hazard_summary(
        hazard_analysis={
            "hazards": ["Flood"],
        },
        multi_hazard_analysis={
            "compound_risks": [],
        },
        priority_results=[
            {
                "hazard": "Flood",
                "risk_score": 90,
                "severity": "Extreme",
                "priority": 1,
            }
        ],
    )

    assert result["hazard_count"] == 1
    assert result["highest_priority_hazard"]["hazard"] == "Flood"
    assert result["status"] == "Hazards Detected"