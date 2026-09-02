from core.hazards.hazard_engine import HazardEngine
from core.hazards.hazard_report import generate_hazard_report


def test_hazard_report():

    engine = HazardEngine()

    analysis = engine.analyze(
        ndvi=0.1,
        ndwi=0.1,
        ndbi=0.1,
        savi=0.1,
        environmental_score=20,
    )

    report = generate_hazard_report(
        analysis
    )

    assert report["hazard_count"] >= 1
    assert "Drought" in report["hazards"]
    assert "environmental_score" in report