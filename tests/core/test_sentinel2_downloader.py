"""
Tests for the Sentinel-2 downloader.
"""

from pathlib import Path

from core.connectors.sentinel2.sentinel2_downloader import (
    Sentinel2Downloader,
)


def test_downloader_initializes() -> None:
    downloader = Sentinel2Downloader()

    assert downloader.provider_name == "Sentinel-2"
    assert downloader.timeout == 120


def test_downloader_health_check() -> None:
    downloader = Sentinel2Downloader()

    health = downloader.health_check()

    assert health["provider"] == "Sentinel-2"
    assert health["available"] is True


def test_invalid_timeout() -> None:
    try:
        Sentinel2Downloader(timeout=0)
        assert False
    except ValueError as exc:
        assert str(exc) == "Timeout must be greater than zero."


def test_invalid_user_agent() -> None:
    try:
        Sentinel2Downloader(user_agent="   ")
        assert False
    except ValueError as exc:
        assert str(exc) == "User agent is required."


def test_product_id_extraction_from_string() -> None:
    downloader = Sentinel2Downloader()

    assert downloader._extract_product_id(
        "S2A_TEST_001"
    ) == "S2A_TEST_001"


def test_product_id_extraction_from_dictionary() -> None:
    downloader = Sentinel2Downloader()

    product = {
        "product_id": "S2A_TEST_002",
    }

    assert downloader._extract_product_id(product) == "S2A_TEST_002"


def test_product_id_extraction_from_object() -> None:
    downloader = Sentinel2Downloader()

    class Product:
        product_id = "S2B_TEST_001"

    assert downloader._extract_product_id(Product()) == "S2B_TEST_001"


def test_missing_product_id() -> None:
    downloader = Sentinel2Downloader()

    result = downloader.download(
        product="",
        destination="data/test.zip",
    )

    assert not result.success
    assert result.error == "Product ID is required"


def test_missing_destination() -> None:
    downloader = Sentinel2Downloader()

    result = downloader.download(
        product="S2A_TEST_001",
        destination=None,
    )

    assert not result.success
    assert result.error == "Destination is required"


def test_missing_download_url() -> None:
    downloader = Sentinel2Downloader()

    result = downloader.download(
        product={
            "product_id": "S2A_TEST_001",
        },
        destination="data/test.zip",
    )

    assert not result.success
    assert result.error == "Download URL is required"


def test_is_available_with_complete_product() -> None:
    downloader = Sentinel2Downloader()

    product = {
        "product_id": "S2A_TEST_001",
        "download_url": "https://example.com/test.zip",
    }

    assert downloader.is_available(product) is True


def test_is_available_without_url() -> None:
    downloader = Sentinel2Downloader()

    product = {
        "product_id": "S2A_TEST_001",
    }

    assert downloader.is_available(product) is False