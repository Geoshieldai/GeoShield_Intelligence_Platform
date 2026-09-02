from core.indices.classifier import (
    classify_ndvi,
    classify_ndwi,
    classify_ndbi,
    classify_savi,
)


def test_ndvi_classifier():

    result = classify_ndvi(0.75)

    assert result.index == "NDVI"
    assert result.classification == "high_vegetation"


def test_ndwi_classifier():

    result = classify_ndwi(0.50)

    assert result.index == "NDWI"
    assert result.classification == "water_likely"


def test_ndbi_classifier():

    result = classify_ndbi(0.30)

    assert result.index == "NDBI"
    assert result.classification == "built_up_likely"


def test_savi_classifier():

    result = classify_savi(0.60)

    assert result.index == "SAVI"
    assert result.classification == "high_vegetation"