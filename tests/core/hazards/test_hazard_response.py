from core.hazards.hazard_engine import HazardEngine
from core.hazards.hazard_response import generate_hazard_response


def test_hazard_response():

    engine = HazardEngine()

    analysis = engine.analyze(
        ndvi=0.1,
        ndwi=0.1,
        ndbi=0.1,
        savi=0.1,
        environmental_score=10,
    )

    response = generate_hazard_response(
        analysis
    )

    assert isinstance(response, list)
    assert len(response) > 0