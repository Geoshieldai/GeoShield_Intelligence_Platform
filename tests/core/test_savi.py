from core.indices.savi import calculate_savi


def test_savi():

    red = 0.2
    nir = 0.6

    savi = calculate_savi(
        red,
        nir,
        soil_adjustment=0.5,
    )

    assert round(savi, 6) == 0.461538