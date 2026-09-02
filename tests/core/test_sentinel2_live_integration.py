"""
Tests for the Sentinel-2 live integration foundation.
"""

import os

import pytest
from dotenv import load_dotenv

load_dotenv()

from core.connectors.sentinel2.sentinel2_auth import Sentinel2Auth
from core.connectors.sentinel2.sentinel2_endpoint import Sentinel2Endpoint
from core.connectors.sentinel2.sentinel2_http import Sentinel2HTTP
from core.connectors.sentinel2.sentinel2_live_status import (
    Sentinel2LiveStatus,
)
from core.connectors.sentinel2.sentinel2_query import Sentinel2Query
from core.connectors.sentinel2.sentinel2_request import Sentinel2Request


def test_auth_configuration():
    auth = Sentinel2Auth(
        client_id="test-client",
        client_secret="test-secret",
    )

    assert auth.is_configured is True
    assert auth.has_token is False
    assert auth.validate() is True


def test_auth_does_not_expose_secret():
    auth = Sentinel2Auth(
        client_id="test-client",
        client_secret="secret",
    )

    data = auth.to_dict()

    assert "client_secret" not in data
    assert "token" not in data
    assert data["configured"] is True


def test_endpoint_urls():
    endpoint = Sentinel2Endpoint()

    assert endpoint.search_url.endswith(
        "/resto/api/collections/Sentinel2"
    )

    assert "identity.dataspace.copernicus.eu" in endpoint.token_url


def test_query_builder():
    request = Sentinel2Request(
        start_date="2026-01-01",
        end_date="2026-01-31",
    )

    query = Sentinel2Query(request)
    params = query.to_params()

    assert params["startDate"] == "2026-01-01"
    assert params["completionDate"] == "2026-01-31"


def test_query_with_filters():
    request = Sentinel2Request(
        start_date="2026-01-01",
        end_date="2026-01-31",
        cloud_cover_max=20.0,
        tile_id="T37MCS",
    )

    query = Sentinel2Query(request)
    params = query.to_params()

    assert params["cloudCover"] == 20.0
    assert params["tileId"] == "T37MCS"


def test_http_search_request():
    http = Sentinel2HTTP()

    request = http.build_search_request(
        {
            "startDate": "2026-01-01",
            "completionDate": "2026-01-31",
        }
    )

    assert request["method"] == "GET"
    assert "url" in request
    assert request["params"]["startDate"] == "2026-01-01"


def test_http_token_request():
    http = Sentinel2HTTP()

    request = http.build_token_request(
        client_id="client",
        client_secret="secret",
    )

    assert request["method"] == "POST"
    assert "token" in request["url"]
    assert request["form"]["grant_type"] == "client_credentials"


def test_live_status_disabled():
    status = Sentinel2LiveStatus()

    assert status.enabled is False
    assert status.authenticated is False
    assert status.network_enabled is False
    assert status.is_live is False


def test_live_status_enabled():
    status = Sentinel2LiveStatus(
        enabled=True,
        authenticated=True,
        network_enabled=True,
    )

    assert status.is_live is True

    data = status.to_dict()

    assert data["is_live"] is True


def test_auth_token_status():
    auth = Sentinel2Auth(token="temporary-token")

    assert auth.has_token is True
    assert auth.validate() is True


def test_live_copernicus_authentication():
    """
    Verify that GeoShield can obtain a real Copernicus token.

    Requires:
        COPERNICUS_CLIENT_ID
        COPERNICUS_CLIENT_SECRET

    from the local .env file.
    """

    client_id = os.getenv("COPERNICUS_CLIENT_ID")
    client_secret = os.getenv("COPERNICUS_CLIENT_SECRET")

    if not client_id or not client_secret:
        pytest.skip(
            "Copernicus credentials are not configured."
        )

    auth = Sentinel2Auth(
        client_id=client_id,
        client_secret=client_secret,
    )

    http = Sentinel2HTTP()

    response = http.request_token(
    client_id=client_id,
    client_secret=client_secret,
)
    assert isinstance(response, dict)

    access_token = response.get("access_token")

    assert isinstance(access_token, str)
    assert access_token

    auth.set_token(
        token=access_token,
        expires_in=response.get("expires_in"),
    )

    assert auth.has_token is True
    assert auth.token_is_valid is True