"""
GeoShield Sentinel-2 Downloader

Authenticated, resumable Sentinel-2 product downloader for the
Copernicus Data Space Ecosystem.

Architecture:

    STAC Product Name
          |
          v
    OData Product Lookup
          |
          v
    Product UUID
          |
          v
    Authenticated Download
          |
          v
    Resumable ZIP
          |
          v
    Verified Final Product

The STAC catalog may expose an S3 path such as:

    s3://eodata/...

That path is metadata and is NOT treated as an HTTP download URL.
The actual product is downloaded through the authenticated CDSE
OData download endpoint.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable
from urllib.parse import quote

import requests

from core.auth.copernicus import CopernicusAuthManager
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
        """Convert the request into a dictionary."""

        return {
            "product_id": self.product_id,
            "destination": self.destination,
            "url": self.url,
        }


class Sentinel2Downloader:
    """
    Authenticated and resumable Sentinel-2 product downloader.

    Features:

        - Copernicus OAuth authentication
        - OData product UUID resolution
        - OData download URL generation
        - Streaming downloads
        - HTTP Range resume support
        - Temporary .part files
        - Retry handling
        - Progress reporting
        - Atomic finalization
        - Download-size validation
        - Safe error reporting
    """

    provider_name = "Sentinel-2"

    ODATA_BASE_URL = (
        "https://catalogue.dataspace.copernicus.eu/odata/v1"
    )

    DOWNLOAD_BASE_URL = (
        "https://download.dataspace.copernicus.eu/odata/v1"
    )

    CHUNK_SIZE = 4 * 1024 * 1024

    DEFAULT_MAX_RETRIES = 3

    def __init__(
        self,
        timeout: int = 120,
        user_agent: str = "GeoShield/0.1.0",
        auth_manager: CopernicusAuthManager | None = None,
        session: requests.Session | None = None,
        transport: Callable[
            [str, Path, int, str],
            None,
        ]
        | None = None,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> None:
        """Initialize the Sentinel-2 downloader."""

        if timeout <= 0:
            raise ValueError(
                "Timeout must be greater than zero."
            )

        if not user_agent.strip():
            raise ValueError(
                "User agent is required."
            )

        if max_retries < 0:
            raise ValueError(
                "max_retries cannot be negative."
            )

        self.timeout = timeout
        self.user_agent = user_agent

        self.auth_manager = (
            auth_manager
            if auth_manager is not None
            else CopernicusAuthManager()
        )

        self.session = (
            session
            if session is not None
            else requests.Session()
        )

        self.transport = transport
        self.max_retries = max_retries

        self.session.headers.update(
            {
                "User-Agent": self.user_agent,
            }
        )

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

    def resolve_product_uuid(
        self,
        product_name: str,
    ) -> str:
        """
        Resolve a Sentinel-2 product name to its Copernicus UUID.

        The STAC catalog returns the product name while the
        OData download API requires the product UUID.
        """

        name = product_name.strip()

        if not name:
            raise ValueError(
                "Product name is required."
            )

        token = self.auth_manager.get_token()

        url = f"{self.ODATA_BASE_URL}/Products"

        escaped_name = name.replace(
            "'",
            "''",
        )

        params = {
            "$filter": f"Name eq '{escaped_name}'",
            "$top": "1",
        }

        response = self.session.get(
            url,
            params=params,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            },
            timeout=self.timeout,
        )

        if not response.ok:
            raise RuntimeError(
                "Copernicus OData product lookup failed "
                f"(HTTP {response.status_code}). "
                f"{self._safe_error_detail(response)}"
            )

        try:
            payload = response.json()
        except ValueError as exc:
            raise RuntimeError(
                "Copernicus OData product lookup returned "
                "invalid JSON."
            ) from exc

        values = payload.get("value", [])

        if not isinstance(values, list):
            raise RuntimeError(
                "Invalid OData response: "
                "'value' is not a list."
            )

        if not values:
            raise RuntimeError(
                "Sentinel-2 product was not found in the "
                "Copernicus OData catalogue: "
                f"{name}"
            )

        product = values[0]

        if not isinstance(product, dict):
            raise RuntimeError(
                "Invalid OData product record."
            )

        product_uuid = product.get("Id")

        if not product_uuid:
            raise RuntimeError(
                "OData product record does not contain an Id."
            )

        return str(product_uuid)

    def build_download_url(
        self,
        product_uuid: str,
    ) -> str:
        """Build the authenticated Copernicus download URL."""

        uuid = product_uuid.strip()

        if not uuid:
            raise ValueError(
                "Product UUID is required."
            )

        return (
            f"{self.DOWNLOAD_BASE_URL}/"
            f"Products({quote(uuid, safe='')})/"
            "$value"
        )

    def download(
        self,
        product: Any,
        destination: str | None = None,
    ) -> ConnectorResult:
        """
        Download a Sentinel-2 product.

        A .part file is used while downloading.

        If a .part file already exists, the downloader attempts
        to resume from the existing byte offset using HTTP Range.
        """

        product_name = self._extract_product_id(product)

        if not product_name:
            return ConnectorResult.failure(
                provider=self.provider_name,
                operation="download",
                error=(
                    "Product ID or product name is required"
                ),
            )

        if not destination:
            return ConnectorResult.failure(
                provider=self.provider_name,
                operation="download",
                error="Destination is required",
            )

        destination_path = Path(destination)
        partial_path = Path(
            f"{destination_path}.part"
        )

        try:
            destination_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            if destination_path.exists():
                existing_size = (
                    destination_path.stat().st_size
                )

                if existing_size > 0:
                    return ConnectorResult.ok(
                        provider=self.provider_name,
                        operation="download",
                        data={
                            "product_id": product_name,
                            "destination": str(
                                destination_path
                            ),
                            "status": "already_downloaded",
                        },
                        metadata={
                            "size_bytes": existing_size,
                        },
                    )

            product_uuid = self.resolve_product_uuid(
                product_name
            )

            download_url = self.build_download_url(
                product_uuid
            )

            token = self.auth_manager.get_token()

            if self.transport is not None:
                self.transport(
                    download_url,
                    destination_path,
                    self.timeout,
                    self.user_agent,
                )
            else:
                size_bytes = (
                    self._download_authenticated_resumable(
                        url=download_url,
                        destination=destination_path,
                        partial_path=partial_path,
                        token=token,
                    )
                )

                if size_bytes <= 0:
                    raise RuntimeError(
                        "Download completed but the "
                        "destination file is empty."
                    )

            if not destination_path.exists():
                raise RuntimeError(
                    "Download reported success but the "
                    "destination file does not exist."
                )

            final_size = destination_path.stat().st_size

            if final_size <= 0:
                raise RuntimeError(
                    "Downloaded file is empty."
                )

            return ConnectorResult.ok(
                provider=self.provider_name,
                operation="download",
                data={
                    "product_id": product_name,
                    "product_uuid": product_uuid,
                    "destination": str(
                        destination_path
                    ),
                    "status": "downloaded",
                },
                metadata={
                    "url": download_url,
                    "size_bytes": final_size,
                    "resumable": True,
                },
            )

        except Exception as exc:
            return ConnectorResult.failure(
                provider=self.provider_name,
                operation="download",
                error=str(exc),
                metadata={
                    "product_id": product_name,
                    "destination": str(
                        destination_path
                    ),
                    "partial_destination": str(
                        partial_path
                    ),
                },
            )

    def _download_authenticated_resumable(
        self,
        url: str,
        destination: Path,
        partial_path: Path,
        token: str,
    ) -> int:
        """
        Stream an authenticated download with resume support.
        """

        existing_size = 0

        if partial_path.exists():
            existing_size = partial_path.stat().st_size

        last_error: Exception | None = None

        for attempt in range(
            1,
            self.max_retries + 2,
        ):
            try:
                headers = {
                    "Authorization": (
                        f"Bearer {token}"
                    ),
                    "Accept": (
                        "application/octet-stream"
                    ),
                }

                if existing_size > 0:
                    headers["Range"] = (
                        f"bytes={existing_size}-"
                    )

                response = self.session.get(
                    url,
                    headers=headers,
                    timeout=self.timeout,
                    stream=True,
                    allow_redirects=True,
                )

                if (
                    existing_size > 0
                    and response.status_code == 200
                ):
                    response.close()

                    existing_size = 0

                    with partial_path.open(
                        "wb"
                    ):
                        pass

                    response = self.session.get(
                        url,
                        headers={
                            "Authorization": (
                                f"Bearer {token}"
                            ),
                            "Accept": (
                                "application/octet-stream"
                            ),
                        },
                        timeout=self.timeout,
                        stream=True,
                        allow_redirects=True,
                    )

                if not response.ok:
                    error = RuntimeError(
                        "Copernicus product download failed "
                        f"(HTTP {response.status_code}). "
                        f"{self._safe_error_detail(response)}"
                    )

                    response.close()
                    raise error

                content_length = response.headers.get(
                    "Content-Length"
                )

                total_bytes: int | None = None

                if content_length:
                    try:
                        response_length = int(
                            content_length
                        )

                        total_bytes = (
                            existing_size
                            + response_length
                        )
                    except ValueError:
                        total_bytes = None

                mode = (
                    "ab"
                    if existing_size > 0
                    and response.status_code == 206
                    else "wb"
                )

                if mode == "wb":
                    existing_size = 0

                downloaded = existing_size

                with response:
                    with partial_path.open(
                        mode
                    ) as output_file:

                        for chunk in response.iter_content(
                            chunk_size=self.CHUNK_SIZE
                        ):
                            if not chunk:
                                continue

                            output_file.write(chunk)
                            downloaded += len(chunk)

                            self._report_progress(
                                downloaded=downloaded,
                                total=total_bytes,
                            )

                if downloaded <= 0:
                    raise RuntimeError(
                        "Copernicus returned an empty "
                        "download."
                    )

                partial_path.replace(
                    destination
                )

                return downloaded

            except (
                requests.RequestException,
                OSError,
                RuntimeError,
            ) as exc:

                last_error = exc

                if attempt >= self.max_retries + 1:
                    break

                token = self.auth_manager.get_token()

        if last_error is not None:
            raise RuntimeError(
                "Sentinel-2 download failed after "
                f"{self.max_retries + 1} attempts: "
                f"{last_error}"
            ) from last_error

        raise RuntimeError(
            "Sentinel-2 download failed."
        )

    @staticmethod
    def _report_progress(
        downloaded: int,
        total: int | None,
    ) -> None:
        """
        Report download progress.

        Uses PowerShell-friendly console output when a
        total size is available.
        """

        downloaded_mb = downloaded / (
            1024 * 1024
        )

        if total and total > 0:
            total_mb = total / (
                1024 * 1024
            )

            percentage = (
                downloaded / total
            ) * 100

            print(
                f"\rSentinel-2 download: "
                f"{percentage:6.2f}% "
                f"({downloaded_mb:,.1f} / "
                f"{total_mb:,.1f} MB)",
                end="",
                flush=True,
            )

        else:
            print(
                f"\rSentinel-2 download: "
                f"{downloaded_mb:,.1f} MB",
                end="",
                flush=True,
            )

    def is_available(
        self,
        product: Any,
    ) -> bool:
        """
        Return whether the supplied object contains a
        usable Sentinel-2 product identifier.
        """

        return bool(
            self._extract_product_id(product)
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
            "odata_base_url": (
                self.ODATA_BASE_URL
            ),
            "download_base_url": (
                self.DOWNLOAD_BASE_URL
            ),
            "resumable": True,
            "chunk_size_bytes": self.CHUNK_SIZE,
            "max_retries": self.max_retries,
        }

    @staticmethod
    def _extract_product_id(
        product: Any,
    ) -> str | None:
        """
        Extract the Sentinel-2 product name.

        GeoShield Sentinel2Product stores the Copernicus
        product name in product_id.
        """

        if isinstance(product, str):
            value = product.strip()
            return value or None

        if isinstance(product, dict):
            value = product.get("product_id")

            if value is None:
                value = product.get(
                    "product_name"
                )

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
                "product_name",
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
    def _safe_error_detail(
        response: requests.Response,
    ) -> str:
        """
        Extract a useful provider error without exposing
        credentials or access tokens.
        """

        try:
            data = response.json()
        except ValueError:
            text = response.text.strip()

            if not text:
                return (
                    "No additional error information "
                    "was returned."
                )

            return text[:500]

        if isinstance(data, dict):
            detail = (
                data.get("detail")
                or data.get("title")
                or data.get("message")
                or data.get("error_description")
                or data.get("error")
            )

            if detail:
                return str(detail)[:500]

        text = response.text.strip()

        if text:
            return text[:500]

        return (
            "No additional error information "
            "was provided."
        )
