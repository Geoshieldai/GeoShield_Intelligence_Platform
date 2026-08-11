"""
GeoShield Sentinel-2 Downloader

Download manager for Sentinel-2 products.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable
from urllib.request import Request, urlopen

from core.connectors.connector_result import ConnectorResult


@dataclass
class Sentinel2DownloadRequest:
    """Standard Sentinel-2 download request."""

    product_id: str
    destination: str
    url: str | None = None

    def validate(self) -> bool:
        """Validate the download request."""

        return bool(
            self.product_id.strip()
            and self.destination.strip()
        )

    def to_dict(self) -> dict[str, str | None]:
        """Convert the request to a dictionary."""

        return {
            "product_id": self.product_id,
            "destination": self.destination,
            "url": self.url,
        }


class Sentinel2Downloader:
    """Download manager for Sentinel-2 products."""

    provider_name = "Sentinel-2"

    def __init__(
        self,
        timeout: int = 120,
        user_agent: str = "GeoShield/0.1.0",
        transport: Callable[
            [str, Path, int, str],
            None,
        ]
        | None = None,
    ) -> None:
        """Initialize the downloader."""

        if timeout <= 0:
            raise ValueError(
                "Timeout must be greater than zero."
            )

        if not user_agent.strip():
            raise ValueError(
                "User agent is required."
            )

        self.timeout = timeout
        self.user_agent = user_agent
        self.transport = transport

    def create_request(
        self,
        product_id: str,
        destination: str,
        url: str | None = None,
    ) -> Sentinel2DownloadRequest:
        """Create and validate a download request."""

        request = Sentinel2DownloadRequest(
            product_id=product_id,
            destination=destination,
            url=url,
        )

        if not request.validate():
            raise ValueError(
                "Valid product ID and destination are required."
            )

        return request

    def prepare(
        self,
        request: Sentinel2DownloadRequest,
    ) -> dict[str, object]:
        """Prepare a download operation."""

        if not request.validate():
            raise ValueError(
                "Invalid Sentinel-2 download request."
            )

        return {
            "status": "download_ready",
            "product_id": request.product_id,
            "destination": request.destination,
            "url": request.url,
        }

    def download(
        self,
        product: Any,
        destination: str | None = None,
    ) -> ConnectorResult:
        """Download a Sentinel-2 product."""

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

        download_url = self._extract_download_url(product)

        if not download_url:
            return ConnectorResult.failure(
                provider=self.provider_name,
                operation="download",
                error="Download URL is required",
            )

        destination_path = Path(destination)

        try:
            destination_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            if self.transport is not None:
                self.transport(
                    download_url,
                    destination_path,
                    self.timeout,
                    self.user_agent,
                )
            else:
                self._download_http(
                    url=download_url,
                    destination=destination_path,
                )

            size_bytes = 0

            if destination_path.exists():
                size_bytes = destination_path.stat().st_size

            return ConnectorResult.ok(
                provider=self.provider_name,
                operation="download",
                data={
                    "product_id": product_id,
                    "destination": str(destination_path),
                    "status": "downloaded",
                },
                metadata={
                    "url": download_url,
                    "size_bytes": size_bytes,
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
                    "url": download_url,
                },
            )

    def is_available(
        self,
        product: Any,
    ) -> bool:
        """Check whether a product can be downloaded."""

        return bool(
            self._extract_product_id(product)
            and self._extract_download_url(product)
        )

    def health_check(self) -> dict[str, Any]:
        """Return downloader health information."""

        return {
            "provider": self.provider_name,
            "available": True,
            "timeout": self.timeout,
            "user_agent": self.user_agent,
            "transport_configured": (
                self.transport is not None
            ),
        }

    def _download_http(
        self,
        url: str,
        destination: Path,
    ) -> None:
        """Download a product using HTTP."""

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
        """Extract a product ID."""

        if isinstance(product, str):
            value = product.strip()
            return value or None

        if isinstance(product, dict):
            value = product.get("product_id")

            if value is None:
                value = product.get("id")

            if value is None:
                return None

            value = str(value).strip()
            return value or None

        value = getattr(
            product,
            "product_id",
            None,
        )

        if value is None:
            value = getattr(
                product,
                "id",
                None,
            )

        if value is None:
            return None

        value = str(value).strip()
        return value or None

    @staticmethod
    def _extract_download_url(
        product: Any,
    ) -> str | None:
        """Extract a download URL."""

        if isinstance(product, dict):
            value = product.get("download_url")

            if value is None:
                value = product.get("url")

            if value is None:
                return None

            value = str(value).strip()
            return value or None

        value = getattr(
            product,
            "download_url",
            None,
        )

        if value is None:
            value = getattr(
                product,
                "url",
                None,
            )

        if value is None:
            return None

        value = str(value).strip()
        return value or None