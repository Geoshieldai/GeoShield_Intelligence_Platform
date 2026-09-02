from core.indices.environmental_response import build_environmental_response


def test_environmental_response():

    result = {
        "indices": {
            "ndvi": 0.6,
            "ndbi": 0.1,
            "ndwi": 0.3,
            "savi": 0.5,
            "evi": None,
        },
        "classifications": {
            "ndvi": "Very Healthy Vegetation",
            "ndbi": "Moderate Built-up Area",
            "ndwi": "Moderate Water Presence",
            "savi": "Dense Vegetation",
        },
        "environmental_score": 75.0,
        "report": {
            "environmental_score": 75.0,
            "condition": "Good Environmental Condition",
            "risk_level": "Moderate Risk",
            "indices": {
                "NDVI": 0.6,
                "NDWI": 0.3,
                "NDBI": 0.1,
                "SAVI": 0.5,
                "EVI": None,
            },
        },
    }

    response = build_environmental_response(result)

    assert response["status"] == "success"
    assert response["environmental_score"] == 75.0
    assert response["condition"] == "Good Environmental Condition"
    assert response["risk_level"] == "Moderate Risk"

    assert "indices" in response
    assert "classifications" in response
    assert "report" in response