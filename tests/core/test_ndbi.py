from core.indices.ndbi import calculate_ndbi


def test_ndbi():

    swir = 0.6
    nir = 0.2

    ndbi = calculate_ndbi(swir, nir)

    assert abs(ndbi - 0.5) < 1e-9