"""Tests for the Sentinel-2 catalog normalization service."""

import pytest

from core.connectors.sentinel2.sentinel2_catalog import (
    Sentinel2Catalog,
)


def test_normalize_product() -> None:
    """A catalog record should normalize into a Sentinel-2 product."""

    catalog = Sentinel2Catalog()

    record = {
        "id": "S2A_TEST_001",
        "datetime": "2026-01-15",
        "processingLevel": "L2A",
        "cloudCover": 12.5,
        "tileId": "T37MCA",
        "name": "Test Sentinel-2 Product",
        "source": "test",
    }

    product = catalog.normalize_product(record)

    assert product.product_id == "S2A_TEST_001"
    assert product.acquisition_date == "2026-01-15"
    assert product.processing_level == "L2A"
    assert product.cloud_cover == 12.5
    assert product.tile_id == "T37MCA"
    assert product.product_name == "Test Sentinel-2 Product"
    assert product.metadata["source"] == "test"


def test_normalize_product_requires_product_id() -> None:
    """A catalog record without an ID should be rejected."""

    catalog = Sentinel2Catalog()

    with pytest.raises(
        ValueError,
        match="Sentinel-2 product ID is required",
    ):
        catalog.normalize_product(
            {
                "datetime": "2026-01-15",
                "processingLevel": "L2A",
            }
        )


def test_normalize_many() -> None:
    """Multiple catalog records should normalize correctly."""

    catalog = Sentinel2Catalog()

    records = [
        {
            "id": "S2A_TEST_001",
            "datetime": "2026-01-15",
            "processingLevel": "L2A",
        },
        {
            "id": "S2B_TEST_002",
            "datetime": "2026-01-16",
            "processingLevel": "L2A",
        },
    ]

    products = catalog.normalize_many(records)

    assert len(products) == 2
    assert products[0].product_id == "S2A_TEST_001"
    assert products[1].product_id == "S2B_TEST_002"