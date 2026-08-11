from core.hazards.intelligence import HazardIntelligence


def test_hazard_intelligence():

    intelligence = HazardIntelligence()

    result = intelligence.analyze(
        ndvi=0.1,
        ndwi=0.1,
        ndbi=0.1,
        savi=0.1,
        environmental_score=20,
    )

    assert "hazard" in result
    assert "multi_hazard" in result

    assert (
        "Drought"
        in result["hazard"]["analysis"]["hazards"]
    )

    assert (
        result["multi_hazard"]["summary"]["hazard_count"]
        >= 1
    )