from core.hazards.risk import HazardRisk


def test_hazard_risk():

    risk = HazardRisk()

    result = risk.calculate(
        hazard="Drought",
        environmental_score=20,
    )

    assert result == 80.0


def test_healthy_environment_has_lower_risk():

    risk = HazardRisk()

    result = risk.calculate(
        hazard="Flood",
        environmental_score=90,
    )

    assert result == 10.0