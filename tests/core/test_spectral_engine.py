from core.indices.spectral_engine import SpectralEngine
from core.indices.spectral_input import SpectralInput


def test_spectral_engine():

    data = SpectralInput(
        red=0.20,
        green=0.30,
        nir=0.70,
        swir=0.40,
    )

    engine = SpectralEngine()

    report = engine.analyze(data)

    assert "NDVI" in report.values
    assert "NDWI" in report.values
    assert "NDBI" in report.values
    assert "SAVI" in report.values

    assert "NDVI" in report.classifications
    assert "NDWI" in report.classifications
    assert "NDBI" in report.classifications
    assert "SAVI" in report.classifications