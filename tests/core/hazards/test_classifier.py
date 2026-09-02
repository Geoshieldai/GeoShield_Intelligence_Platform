from core.hazards.classifier import HazardClassifier


def test_hazard_classifier():

    classifier = HazardClassifier()

    result = classifier.classify(
        ["Drought", "Flood"]
    )

    assert "Drought" in result
    assert "Flood" in result

    assert result["Drought"]["category"] == "Climate"
    assert result["Flood"]["category"] == "Hydrological"