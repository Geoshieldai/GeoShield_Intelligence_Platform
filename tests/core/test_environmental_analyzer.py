from core.environmental.analyzer import EnvironmentalAnalyzer


def test_environmental_analyzer():

    analyzer = EnvironmentalAnalyzer()

    result = analyzer.analyze(
        ndvi=0.6,
        ndbi=0.1,
        ndwi=0.3,
        savi=0.5,
    )

    assert result["status"] == "success"

    assert "environmental_score" in result
    assert "condition" in result
    assert "risk_level" in result
    assert "indices" in result
    assert "classifications" in result
    assert "report" in result

    assert 0 <= result["environmental_score"] <= 100