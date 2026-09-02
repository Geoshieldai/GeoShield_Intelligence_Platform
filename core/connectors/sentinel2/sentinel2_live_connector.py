"""
GeoShield Sentinel-2 Live Connector

Live integration bridge between the Sentinel-2 service layer
and the Copernicus Data Space provider.
"""

from __future__ import annotations

from typing import Any

from .sentinel2_auth import Sentinel2Auth
from .sentinel2_http import Sentinel2HTTP
from .sentinel2_query import Sentinel2Query
from .sentinel2_request import Sentinel2Request
from .sentinel2_service import Sentinel2Service


class Sentinel2LiveConnector:
    """
    Live Sentinel-2 provider connector.

    Handles authentication, catalog searches, and product
    normalization while keeping credentials out of responses.
    """

    def __init__(
        self,
        auth: Sentinel2Auth | None = None,
        http: Sentinel2HTTP | None = None,
        service: Sentinel2Service | None = None,
    ) -> None:
        self.auth = auth or Sentinel2Auth()
        self.http = http or Sentinel2HTTP()
        self.service = service or Sentinel2Service()

    def status(self) -> dict[str, bool]:
        """
        Return authentication and live-readiness information.
        """

        return {
            "authentication_configured": self.auth.is_configured,
            "token_available": self.auth.has_token,
            "live_ready": self.auth.validate(),
        }

    def authenticate(self) -> dict[str, Any]:
        """
        Authenticate with Copernicus Data Space.

        Stores the returned access token internally and returns
        only safe authentication status information.
        """

        if not self.auth.client_id or not self.auth.client_secret:
            raise ValueError(
                "Sentinel-2 client credentials are required."
            )

        response = self.http.request_token(
            client_id=self.auth.client_id,
            client_secret=self.auth.client_secret,
        )

        token = response.get("access_token")

        if not isinstance(token, str) or not token:
            raise ValueError(
                "Copernicus token response did not contain "
                "a valid access token."
            )

        self.auth.token = token

        return {
            "authenticated": True,
            "token_available": True,
            "token_type": response.get("token_type"),
            "expires_in": response.get("expires_in"),
        }

    def prepare_search(
        self,
        request: Sentinel2Request,
    ) -> dict[str, Any]:
        """
        Prepare an authenticated Sentinel-2 catalog search.
        """

        query = Sentinel2Query(request)
        params = query.to_params()

        return self.http.build_search_request(params)

    def search(
        self,
        request: Sentinel2Request,
    ) -> dict[str, Any]:
        """
        Execute an authenticated Sentinel-2 catalog search.
        """

        if not self.auth.token:
            self.authenticate()

        if not self.auth.token:
            raise ValueError(
                "Authentication failed: no access token available."
            )

        query = Sentinel2Query(request)
        params = query.to_params()

        return self.http.search(
            params=params,
            token=self.auth.token,
        )

    def normalize_records(
        self,
        records: list[dict[str, Any]],
    ):
        """
        Normalize live-provider records into GeoShield products.
        """

        return self.service.normalize_products(records)