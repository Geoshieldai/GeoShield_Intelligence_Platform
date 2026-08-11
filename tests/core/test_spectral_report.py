from core.indices.spectral_report import SpectralReport


def test_spectral_report():

    report = SpectralReport(
        values={
            "NDVI": 0.5,
            "NDWI": 0.2,
        },
        classifications={
            "NDVI": "moderate_vegetation",
            "NDWI": "water_not_detected",
        },
    )

    assert report.values["NDVI"] == 0.5
    assert report.values["NDWI"] == 0.2

    assert report.classifications["NDVI"] == "moderate_vegetation"
    assert report.classifications["NDWI"] == "water_not_detected"