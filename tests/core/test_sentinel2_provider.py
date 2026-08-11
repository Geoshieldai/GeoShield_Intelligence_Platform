"""
Tests for the GeoShield Sentinel-2 provider integration layer.
"""

from core.connectors.sentinel2.sentinel2_client import Sentinel2Client
from core.connectors.sentinel2.sentinel2_metadata import Sentinel2Metadata
from core.connectors.sentinel2.sentinel2_provider import Sentinel2Provider
from core.connectors.sentinel2.sentinel2_request import Sentinel2Request
from core.connectors.sentinel2.sentinel2_response import Sentinel2Response


def test_provider_description():
    provider = Sentinel2Provider()

    description = provider.describe()

    assert description["name"] == "Copernicus Data Space"
    assert description["collection"] == "SENTINEL-2"
    assert description["enabled"] is True


def test_provider_available():
    provider = Sentinel2Provider()

    assert provider.is_available() is True


def test_valid_search_request():
    request = Sentinel2Request(
        start_date="2026-01-01",
        end_date="2026-01-31",
        cloud_cover_max=20,
    )

    assert request.validate() is True


def test_invalid_cloud_cover():
    request = Sentinel2Request(
        start_date="2026-01-01",
        end_date="2026-01-31",
        cloud_cover_max=120,
    )

    assert request.validate() is False


def test_valid_bbox():
    request = Sentinel2Request(
        start_date="2026-01-01",
        end_date="2026-01-31",
        bbox=(36.7, -1.4, 37.0, -1.1),
    )

    assert request.validate() is True


def test_invalid_bbox():
    request = Sentinel2Request(
        start_date="2026-01-01",
        end_date="2026-01-31",
        bbox=(37.0, -1.1, 36.7, -1.4),
    )

    assert request.validate() is False


def test_client_builds_search_request():
    client = Sentinel2Client()

    request = Sentinel2Request(
        start_date="2026-01-01",
        end_date="2026-01-31",
        cloud_cover_max=30,
    )

    payload = client.build_search_request(request)

    assert payload["collection"] == "SENTINEL-2"
    assert payload["cloud_cover_max"] == 30


def test_client_search():
    client = Sentinel2Client()

    request = Sentinel2Request(
        start_date="2026-01-01",
        end_date="2026-01-31",
    )

    response = client.search(request)

    assert isinstance(response, Sentinel2Response)
    assert response.success is True
    assert response.operation == "search"


def test_client_health_check():
    client = Sentinel2Client()

    response = client.health_check()

    assert response.success is True
    assert response.operation == "health_check"


def test_metadata_validation():
    metadata = Sentinel2Metadata(
        product_id="S2A_TEST_PRODUCT",
        acquisition_date="2026-01-01",
        tile_id="T37MCS",
        cloud_cover=12.5,
        processing_level="L2A",
    )

    assert metadata.validate() is True


def test_metadata_dictionary():
    metadata = Sentinel2Metadata(
        product_id="S2A_TEST_PRODUCT",
        acquisition_date="2026-01-01",
    )

    result = metadata.to_dict()

    assert result["product_id"] == "S2A_TEST_PRODUCT"
    assert result["platform"] == "Sentinel-2"
    assert result["instrument"] == "MSI"