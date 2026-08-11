from core.hazards.detector import HazardDetector


def test_detector_detects_drought():

    detector = HazardDetector()

    hazards = detector.detect(
        ndvi=0.1,
        ndwi=0.1,
        ndbi=0.1,
        savi=0.1,
    )

    assert "Drought" in hazards


def test_detector_detects_flood():

    detector = HazardDetector()

    hazards = detector.detect(
        ndvi=0.5,
        ndwi=0.6,
        ndbi=0.1,
        savi=0.4,
    )

    assert "Flood" in hazards