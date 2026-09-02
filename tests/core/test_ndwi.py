from core.indices.ndwi import calculate_ndwi


def test_ndwi():

    green = 0.5
    nir = 0.2

    ndwi = calculate_ndwi(green, nir)

    assert ndwi == 0.4285714285714286