from core.hazards.severity import HazardSeverity


def test_extreme_severity():

    severity = HazardSeverity()

    assert severity.calculate(
        "Flood",
        90,
    ) == "Extreme"


def test_moderate_severity():

    severity = HazardSeverity()

    assert severity.calculate(
        "Drought",
        50,
    ) == "Moderate"


def test_minimal_severity():

    severity = HazardSeverity()

    assert severity.calculate(
        "Flood",
        10,
    ) == "Minimal"