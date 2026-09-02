from core.indices.ndvi import calculate_ndvi


def test_ndvi():

    red = 0.2
    nir = 0.6

    ndvi = calculate_ndvi(red, nir)

    assert abs(ndvi - 0.5) < 1e-9