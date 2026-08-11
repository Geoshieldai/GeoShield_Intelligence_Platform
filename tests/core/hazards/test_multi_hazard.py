from core.hazards.multi_hazard import MultiHazardAnalyzer


def test_multi_hazard_analysis():

    analyzer = MultiHazardAnalyzer()

    result = analyzer.analyze({
        "hazards": [
            "Drought",
            "Vegetation Degradation",
        ],
        "hazard_results": {},
    })

    assert result["hazard_count"] == 2
    assert len(result["compound_risks"]) == 1

    assert (
        result["compound_risks"][0]["type"]
        == "Environmental Stress"
    )