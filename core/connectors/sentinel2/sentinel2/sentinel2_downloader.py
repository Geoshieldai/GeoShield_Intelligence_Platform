"""
GeoShield Sentinel-2 Downloader

Download manager for Sentinel-2 products.

This component is responsible for downloading Sentinel-2 products
to a local destination while keeping download logic independent
from the high-level Sentinel-2 connector.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

from core.connectors.connector_result import ConnectorResult


@dataclass
class Sentinel2DownloadRequest:
    """Parameters used to download a Sentinel-2 product."""

    product_id: str
    destination: str
    url: str | None = None


class Sentinel2Downloader:
    """
    Download Sentinel-2 products.

    The downloader supports:
        - Product ID validation
        - Destination validation
        - URL-based downloads
        - Existing-file detection
        - Download result normalization
    """

    provider_name = "Sentinel-2"

    def __init__(
        self,
        timeout: int = 120,
        user_agent: str = "GeoShield/0.1.0",
    ) -> None:
        """Initialize the Sentinel-2 downloader."""

        if timeout <= 0:
            raise ValueError("Timeout must be greater than zero.")

        if not user_agent.strip():
            raise ValueError("User agent is required.")

        self.timeout = timeout
        self.user_agent = user_agent

    def download(
        self,
        product: Any,
        destination: str | None = None,
    ) -> ConnectorResult:
        """
        Download a Sentinel-2 product.

        Args:
            product:
                Sentinel2Product, product ID string, or a dictionary
                containing product information.

            destination:
                Local destination path.

        Returns:
            ConnectorResult describing the download.
        """

        product_id = self._extract_product_id(product)

        if not product_id:
            return ConnectorResult.failure(
                provider=self.provider_name,
                operation="download",
                error="Product ID is required",
            )

        if not destination:
            return ConnectorResult.failure(
                provider=self.provider_name,
                operation="download",
                error="Destination is required",
            )

        destination_path = Path(destination)

        try:
            destination_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )
        except OSError as exc:
            return ConnectorResult.failure(
                provider=self.provider_name,
                operation="download",
                error=f"Unable to create destination directory: {exc}",
            )

        url = self._extract_url(product)

        if not url:
            return ConnectorResult.failure(
                provider=self.provider_name,
                operation="download",
                error="Download URL is required",
            )

        try:
            self._download_url(
                url=url,
                destination=destination_path,
            )

            return ConnectorResult.ok(
                provider=self.provider_name,
                operation="download",
                data={
                    "product_id": product_id,
                    "destination": str(destination_path),
                    "status": "downloaded",
                },
                metadata={
                    "url": url,
                    "size_bytes": destination_path.stat().st_size,
                },
            )

        except Exception as exc:
            return ConnectorResult.failure(
                provider=self.provider_name,
                operation="download",
                error=str(exc),
                metadata={
                    "product_id": product_id,
                    "destination": str(destination_path),
                    "url": url,
                },
            )

    def is_available(
        self,
        product: Any,
    ) -> bool:
        """Return whether a product contains enough information to download."""

        product_id = self._extract_product_id(product)
        url = self._extract_url(product)

        return bool(product_id and url)

    def health_check(self) -> dict[str, Any]:
        """Return downloader health information."""

        return {
            "provider": self.provider_name,
            "available": True,
            "timeout": self.timeout,
            "user_agent": self.user_agent,
        }

    def _download_url(
        self,
        url: str,
        destination: Path,
    ) -> None:
        """Download a URL to a local file."""

        request = Request(
            url,
            headers={
                "User-Agent": self.user_agent,
            },
        )

        with urlopen(
            request,
            timeout=self.timeout,
        ) as response:
            with destination.open("wb") as output_file:
                while True:
                    chunk = response.read(1024 * 1024)

                    if not chunk:
                        break

                    output_file.write(chunk)

    @staticmethod
    def _extract_product_id(
        product: Any,
    ) -> str | None:
        """Extract a product ID from supported product representations."""

        if isinstance(product, str):
            return product.strip() or None

        if isinstance(product, dict):
            value = product.get("product_id")

            if value is None:
                value = product.get("id")

            return str(value).strip() if value else None

        value = getattr(product, "product_id", None)

        if value is None:
            value = getattr(product, "id", None)

        return str(value).strip() if value else None

    @staticmethod
    def _extract_url(
        product: Any,
    ) -> str | None:
        """Extract a download URL from supported product representations."""

        if isinstance(product, dict):
            value = product.get("download_url")

            if value is None:
                value = product.get("url")

            return str(value).strip() if value else None

        value = getattr(product, "download_url", None)

        if value is None:
            value = getattr(product, "url", None)

        return str(value).strip() if value else None