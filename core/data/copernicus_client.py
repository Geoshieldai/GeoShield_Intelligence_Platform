"""
GeoShield AI Enterprise
Copernicus Data Space Catalogue Client
"""

from __future__ import annotations

from typing import Any

import httpx

from core.auth import CopernicusAuthManager
from core.config import settings


class CopernicusCatalogueClient:
    """GeoShield client for the Copernicus Data Space catalogue."""

    def __init__(
        self,
        auth_manager: CopernicusAuthManager | None = None,
        timeout: float | None = None,
    ) -> None:
        self.auth_manager = auth_manager or CopernicusAuthManager()
        self.timeout = timeout or settings.http_timeout
        self.base_url = settings.cdse_catalog_url

    def _headers(self) -> dict[str, str]:
        """Build authenticated request headers."""

        token = self.auth_manager.get_token()

        return {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "User-Agent": "GeoShield-AI/0.1",
        }

    def _get(
        self,
        params: dict[str, str],
    ) -> list[dict[str, Any]]:
        """Execute an authenticated catalogue GET request."""

        headers = self._headers()

        with httpx.Client(
            timeout=self.timeout,
            headers=headers,
        ) as client:
            response = client.get(
                self.base_url,
                params=params,
            )

        response.raise_for_status()

        payload = response.json()

        return payload.get("value", [])

    def list_products(
        self,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """Return products from the Copernicus catalogue."""

        if limit < 1:
            raise ValueError("limit must be at least 1")

        return self._get(
            {
                "$top": str(limit),
            }
        )

    def search_sentinel2(
        self,
        start_date: str,
        end_date: str,
        limit: int = 10,
        cloud_cover: float | None = 20.0,
    ) -> list[dict[str, Any]]:
        """
        Search the CDSE catalogue for Sentinel-2 products.

        Dates must use YYYY-MM-DD format.
        Cloud cover is expressed as a percentage.
        """

        if limit < 1:
            raise ValueError("limit must be at least 1")

        if cloud_cover is not None and not 0 <= cloud_cover <= 100:
            raise ValueError(
                "cloud_cover must be between 0 and 100"
            )

        filters = [
            "Collection/Name eq 'SENTINEL-2'",
            (
                f"ContentDate/Start gt "
                f"{start_date}T00:00:00.000Z"
            ),
            (
                f"ContentDate/Start lt "
                f"{end_date}T23:59:59.999Z"
            ),
        ]

        if cloud_cover is not None:
            filters.insert(
                1,
                (
                    "Attributes/"
                    "OData.CSC.DoubleAttribute/any("
                    "att:att/Name eq 'cloudCover' and "
                    f"att/OData.CSC.DoubleAttribute/Value "
                    f"le {cloud_cover}"
                    ")"
                ),
            )

        params = {
            "$filter": " and ".join(filters),
            "$top": str(limit),
            "$orderby": "ContentDate/Start desc",
        }

        return self._get(params)


CopernicusClient = CopernicusCatalogueClient


__all__ = [
    "CopernicusCatalogueClient",
    "CopernicusClient",
]