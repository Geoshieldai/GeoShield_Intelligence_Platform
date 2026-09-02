"""
GeoShield AI Enterprise
Copernicus Data Space HTTP Client
"""

from __future__ import annotations

import requests

from core.auth import CopernicusAuthManager
from core.config import settings


class CopernicusClient:
    """Authenticated HTTP client for Copernicus Data Space."""

    def __init__(
        self,
        auth_manager: CopernicusAuthManager | None = None,
    ) -> None:
        self.auth = auth_manager or CopernicusAuthManager()

        self.session = requests.Session()

        self.session.headers.update(
            {
                "Accept": "application/json",
                "User-Agent": "GeoShield-AI-Enterprise/1.0",
            }
        )

    def get(
        self,
        url: str,
        *,
        params: dict | None = None,
    ) -> requests.Response:
        """Perform an authenticated GET request."""

        token = self.auth.get_token()

        headers = {
            "Authorization": f"Bearer {token}",
        }

        return self.session.get(
            url,
            params=params,
            headers=headers,
            timeout=settings.http_timeout,
        )

    def close(self) -> None:
        """Close the HTTP session."""

        self.session.close()

    def __enter__(self) -> "CopernicusClient":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()
