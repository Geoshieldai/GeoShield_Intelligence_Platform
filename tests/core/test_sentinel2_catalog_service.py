"""
Tests for the Sentinel-2 catalog service.
"""

from unittest.mock import Mock, patch

import pytest

from core.connectors.sentinel2.sentinel2_auth import Sentinel2Auth
from core.connectors.sentinel2.sentinel2_catalog_service import (
    Sentinel2CatalogService,
)
from core.connectors.sentinel2.sentinel2_http import Sentinel2HTTP


def create_test_service():
    """
    Create a Sentinel2CatalogService with mocked authentication.

    Unit tests must not contact the real Copernicus OAuth service.
    """

    auth = Sentinel2Auth(
        client_id="test-client-id",
        client_secret="test-client-secret",
    )

    http = Mock(spec=Sentinel2HTTP)

    http.request_token.return_value = {
        "access_token": "test-access-token",
        "expires_in": 3600,
    }

    service = Sentinel2CatalogService(
        auth=auth,
        http=http,
    )

    return service, auth, http


def test_build_search_request():
    service = Sentinel2CatalogService()

    request = service.build_search_request(
        start_date="2026-01-01",
        end_date="2026-01-31",
        cloud_cover_max=20.0,
        limit=10,
    )

    assert request["method"] == "POST"

    assert request["url"] == (
        "https://sh.dataspace.copernicus.eu/catalog/v1/search"
    )

    payload = request["json"]

    assert payload["collections"] == [
        "sentinel-2-l2a"
    ]

    assert payload["datetime"] == (
        "2026-01-01T00:00:00Z/"
        "2026-01-31T23:59:59Z"
    )

    assert payload["limit"] == 10

    assert payload["filter"] == (
        "eo:cloud_cover <= 20.0"
    )


def test_build_search_request_with_bbox():
    service = Sentinel2CatalogService()

    request = service.build_search_request(
        start_date="2026-01-01",
        end_date="2026-01-31",
        bbox=[
            36.5,
            -1.5,
            37.5,
            -0.5,
        ],
    )

    assert request["json"]["bbox"] == [
        36.5,
        -1.5,
        37.5,
        -0.5,
    ]


def test_invalid_date_format():
    service = Sentinel2CatalogService()

    with pytest.raises(ValueError):
        service.build_search_request(
            start_date="01-01-2026",
            end_date="2026-01-31",
        )


def test_invalid_date_order():
    service = Sentinel2CatalogService()

    with pytest.raises(ValueError):
        service.build_search_request(
            start_date="2026-02-01",
            end_date="2026-01-01",
        )


def test_invalid_cloud_cover():
    service = Sentinel2CatalogService()

    with pytest.raises(ValueError):
        service.build_search_request(
            start_date="2026-01-01",
            end_date="2026-01-31",
            cloud_cover_max=101,
        )


def test_invalid_limit():
    service = Sentinel2CatalogService()

    with pytest.raises(ValueError):
        service.build_search_request(
            start_date="2026-01-01",
            end_date="2026-01-31",
            limit=0,
        )


def test_invalid_bbox():
    service = Sentinel2CatalogService()

    with pytest.raises(ValueError):
        service.build_search_request(
            start_date="2026-01-01",
            end_date="2026-01-31",
            bbox=[36.5, -1.5],
        )


@patch(
    "core.connectors.sentinel2."
    "sentinel2_catalog_service.requests.post"
)
def test_search_normalizes_catalog_items(mock_post):
    service, auth, http = create_test_service()

    response = Mock()
    response.ok = True

    response.json.return_value = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "id": "S2A_TEST_PRODUCT",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [],
                },
                "properties": {
                    "datetime": "2026-01-15T08:30:00Z",
                    "eo:cloud_cover": 12.5,
                    "processing:level": "L2A",
                    "title": "S2A_TEST_PRODUCT",
                    "s2:mgrs_tile": "37MCS",
                },
                "assets": {
                    "B04": {
                        "href": (
                            "https://example.com/B04.jp2"
                        )
                    }
                },
                "links": [],
            }
        ],
    }

    mock_post.return_value = response

    products = service.search(
        start_date="2026-01-01",
        end_date="2026-01-31",
        cloud_cover_max=20.0,
        limit=10,
    )

    assert len(products) == 1

    product = products[0]

    assert product.product_id == "S2A_TEST_PRODUCT"

    assert product.acquisition_date == (
        "2026-01-15T08:30:00Z"
    )

    assert product.processing_level == "L2A"

    assert product.cloud_cover == 12.5

    assert product.tile_id == "37MCS"

    http.request_token.assert_called_once_with(
        client_id="test-client-id",
        client_secret="test-client-secret",
    )

    mock_post.assert_called_once()


@patch(
    "core.connectors.sentinel2."
    "sentinel2_catalog_service.requests.post"
)
def test_search_sends_expected_catalog_payload(mock_post):
    service, auth, http = create_test_service()

    response = Mock()
    response.ok = True

    response.json.return_value = {
        "type": "FeatureCollection",
        "features": [],
    }

    mock_post.return_value = response

    service.search(
        start_date="2026-01-01",
        end_date="2026-01-31",
        cloud_cover_max=15.0,
        limit=5,
    )

    _, kwargs = mock_post.call_args

    assert kwargs["headers"]["Authorization"] == (
        "Bearer test-access-token"
    )

    payload = kwargs["json"]

    assert payload["collections"] == [
        "sentinel-2-l2a"
    ]

    assert payload["limit"] == 5

    assert payload["datetime"] == (
        "2026-01-01T00:00:00Z/"
        "2026-01-31T23:59:59Z"
    )

    assert payload["filter"] == (
        "eo:cloud_cover <= 15.0"
    )


@patch(
    "core.connectors.sentinel2."
    "sentinel2_catalog_service.requests.post"
)
def test_search_provider_error(mock_post):
    service, auth, http = create_test_service()

    response = Mock()
    response.ok = False
    response.status_code = 500
    response.text = "Internal server error"

    response.json.side_effect = ValueError

    mock_post.return_value = response

    with pytest.raises(RuntimeError) as exc_info:
        service.search(
            start_date="2026-01-01",
            end_date="2026-01-31",
        )

    assert "HTTP 500" in str(exc_info.value)

    assert (
        "Copernicus Sentinel-2 catalog search failed"
        in str(exc_info.value)
    )