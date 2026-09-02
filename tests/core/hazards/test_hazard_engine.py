from core.hazards.hazard_engine import HazardEngine


def test_hazard_engine_detects_drought():

    engine = HazardEngine()

    result = engine.analyze(
        ndvi=0.1,
        ndwi=0.1,
        ndbi=0.1,
        savi=0.1,
        environmental_score=20,
    )

    assert "Drought" in result["hazards"]
    assert "Drought" in result["hazard_results"]


def test_hazard_engine_detects_flood():

    engine = HazardEngine()

    result = engine.analyze(
        ndvi=0.5,
        ndwi=0.6,
        ndbi=0.1,
        savi=0.4,
        environmental_score=50,
    )

    assert "Flood" in result["hazards"]