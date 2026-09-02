from core.indices.spectral_input import SpectralInput


def test_spectral_input():

    data = SpectralInput(
        red=0.20,
        green=0.30,
        nir=0.70,
        swir=0.40,
    )

    assert data.red == 0.20
    assert data.green == 0.30
    assert data.nir == 0.70
    assert data.swir == 0.40