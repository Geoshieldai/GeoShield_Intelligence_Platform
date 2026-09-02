"""
GeoShield Sentinel-2 HTTP Layer

HTTP communication layer for the Copernicus Data Space
Sentinel-2 integration.

This module handles:
- Search request preparation
- OAuth2 token requests
- Safe error reporting
- Authentication responses

Secrets and access tokens are never included in error messages.
"""

from __future__ import annotations

from typing import Any

import requests

from .sentinel2_endpoint import Sentinel2Endpoint


class Sentinel2HTTP:
    """
    HTTP abstraction for Sentinel-2 provider communication.
    """

    def __init__(
        self,
        endpoint: Sentinel2Endpoint | None = None,
        timeout: int = 30,
    ) -> None:
        self.endpoint = endpoint or Sentinel2Endpoint()
        self.timeout = timeout

    def build_search_request(
        self,
        params: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Build a search request without sending it.
        """

        return {
            "method": "GET",
            "url": self.endpoint.search_url,
            "params": dict(params),
        }

    def build_token_request(
        self,
        client_id: str,
        client_secret: str,
    ) -> dict[str, Any]:
        """
        Build an OAuth2 token request without sending it.

        Credentials are included in the request structure because
        this method is intended for internal HTTP execution.
        """

        if not client_id or not client_secret:
            raise ValueError(
                "Client ID and client secret are required."
            )

        return {
            "method": "POST",
            "url": self.endpoint.token_url,
            "form": {
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
            },
        }

    def request_token(
        self,
        client_id: str,
        client_secret: str,
    ) -> dict[str, Any]:
        """
        Request a real OAuth2 access token from Copernicus Data Space.

        Raises:
            ValueError:
                When credentials are missing.

            RuntimeError:
                When Copernicus rejects the authentication request
                or returns an invalid response.

        The actual client secret and access token are never exposed
        in raised error messages.
        """

        if not client_id or not client_secret:
            raise ValueError(
                "Client ID and client secret are required."
            )

        response = requests.post(
            self.endpoint.token_url,
            data={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
            },
            timeout=self.timeout,
        )

        if not response.ok:
            error_detail = self._safe_error_detail(response)

            raise RuntimeError(
                "Copernicus authentication failed "
                f"(HTTP {response.status_code}). "
                f"{error_detail}"
            )

        try:
            data = response.json()
        except ValueError as exc:
            raise RuntimeError(
                "Copernicus returned an invalid JSON response."
            ) from exc

        access_token = data.get("access_token")

        if not isinstance(access_token, str) or not access_token:
            raise RuntimeError(
                "Copernicus authentication response did not "
                "contain a valid access token."
            )

        return data

    @staticmethod
    def _safe_error_detail(
        response: requests.Response,
    ) -> str:
        """
        Extract a useful authentication error without exposing
        credentials or tokens.
        """

        try:
            data = response.json()
        except ValueError:
            text = response.text.strip()

            if not text:
                return "No additional error information was returned."

            return text[:500]

        error = data.get("error")
        description = data.get("error_description")

        if error and description:
            return f"{error}: {description}"

        if error:
            return str(error)

        if description:
            return str(description)

        return "No additional error information was returned."