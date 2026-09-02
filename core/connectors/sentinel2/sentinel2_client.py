"""
GeoShield Sentinel-2 Client

Client responsible for communicating with the Sentinel-2
provider.

The current implementation provides a safe architecture
for provider communication. Actual HTTP/API requests will
be enabled in the live integration phase.
"""

from __future__ import annotations

from typing import Any

from .sentinel2_provider import Sentinel2Provider
from .sentinel2_request import Sentinel2Request
from .sentinel2_response import Sentinel2Response


class Sentinel2Client:
    """
    Client used to communicate with a Sentinel-2 provider.
    """

    def __init__(
        self,
        provider: Sentinel2Provider | None = None,
    ) -> None:
        self.provider = provider or Sentinel2Provider()

    def provider_info(self) -> dict[str, Any]:
        """
        Return information about the configured provider.
        """
        return self.provider.describe()

    def build_search_request(
        self,
        request: Sentinel2Request,
    ) -> dict[str, Any]:
        """
        Build a provider-ready search request.

        This method does not contact the network.
        """

        if not request.validate():
            raise ValueError(
                "Invalid Sentinel-2 search request."
            )

        return request.to_dict()

    def search(
        self,
        request: Sentinel2Request,
    ) -> Sentinel2Response:
        """
        Prepare a Sentinel-2 search operation.

        Live API communication will be implemented later.
        """

        payload = self.build_search_request(request)

        return Sentinel2Response.success_response(
            operation="search",
            provider=self.provider.provider_name,
            data={
                "status": "request_ready",
                "request": payload,
            },
        )

    def health_check(self) -> Sentinel2Response:
        """
        Check whether the provider is enabled.

        This is an architectural health check only.
        """

        if not self.provider.is_available():
            return Sentinel2Response.failure(
                operation="health_check",
                provider=self.provider.provider_name,
                error="Sentinel-2 provider is disabled.",
            )

        return Sentinel2Response.success_response(
            operation="health_check",
            provider=self.provider.provider_name,
            data={
                "status": "available",
            },
        )