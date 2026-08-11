"""
GeoShield Sentinel-2 Connector

High-level connector for Sentinel-2 satellite data.

This component connects the GeoShield core platform to the
Sentinel-2 catalog service and provides a consistent interface
for searching, normalizing, downloading, and validating
Sentinel-2 products.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.connectors.connector_result import ConnectorResult

from .sentinel2_catalog import Sentinel2Catalog
from .sentinel2_catalog_service import Sentinel2CatalogService
from .sentinel2_product import Sentinel2Product


@dataclass
class Sentinel2SearchRequest:
    """Parameters used to search the Sentinel-2 catalog."""

    start_date: str
    end_date: str
    cloud_cover_max: float | None = None
    limit: int = 10
    bbox: list[float] | None = None


class Sentinel2Connector:
    """
    High-level Sentinel-2 data connector.

    Provides:

        - Sentinel-2 catalog searches
        - Product normalization
        - Product downloading
        - Connection validation
        - Health status
    """

    provider_name = "Sentinel-2"

    def __init__(
        self,
        catalog: Sentinel2Catalog | None = None,
        catalog_service: Sentinel2CatalogService | None = None,
        downloader: Any | None = None,
    ) -> None:
        """Initialize the Sentinel-2 connector."""

        self.catalog = (
            catalog
            if catalog is not None
            else Sentinel2Catalog()
        )

        self.catalog_service = (
            catalog_service
            if catalog_service is not None
            else Sentinel2CatalogService()
        )

        self.downloader = downloader

    def is_enabled(self) -> bool:
        """Return whether the Sentinel-2 connector is enabled."""

        return (
            self.catalog is not None
            and self.catalog_service is not None
        )

    def search(
        self,
        start_date: str,
        end_date: str,
        latitude: float | None = None,
        longitude: float | None = None,
        cloud_cover_max: float | None = None,
        limit: int = 10,
        bbox: list[float] | None = None,
    ) -> ConnectorResult:
        """
        Search the live Sentinel-2 catalog.

        Latitude/longitude can be supplied as a convenience
        location and are converted into a small bounding box
        when no bbox is explicitly provided.
        """

        try:
            if (
                bbox is None
                and latitude is not None
                and longitude is not None
            ):
                delta = 0.01

                bbox = [
                    longitude - delta,
                    latitude - delta,
                    longitude + delta,
                    latitude + delta,
                ]

            products = self.catalog_service.search(
                start_date=start_date,
                end_date=end_date,
                cloud_cover_max=cloud_cover_max,
                limit=limit,
                bbox=bbox,
            )

            return ConnectorResult.ok(
                provider=self.provider_name,
                operation="search",
                data={
                    "status": "search_ready",
                    "products": products,
                },
                metadata={
                    "count": len(products),
                    "start_date": start_date,
                    "end_date": end_date,
                    "cloud_cover_max": cloud_cover_max,
                    "limit": limit,
                    "bbox": bbox,
                },
            )

        except Exception as exc:
            return ConnectorResult.failure(
                provider=self.provider_name,
                operation="search",
                error=str(exc),
            )

    def normalize_product(
        self,
        record: dict[str, Any],
    ) -> Sentinel2Product:
        """Normalize a raw Sentinel-2 catalog record."""

        return self.catalog.normalize_product(record)

    def normalize_many(
        self,
        records: list[dict[str, Any]],
    ) -> list[Sentinel2Product]:
        """Normalize multiple Sentinel-2 catalog records."""

        return self.catalog.normalize_many(records)

    def create_product(
        self,
        product_id: str,
        acquisition_date: str,
        cloud_cover: float | None = None,
        tile_id: str | None = None,
        product_name: str | None = None,
        processing_level: str = "L2A",
        metadata: dict[str, Any] | None = None,
    ) -> Sentinel2Product:
        """Create a normalized Sentinel-2 product."""

        if not product_id:
            raise ValueError(
                "Sentinel-2 product ID is required."
            )

        return Sentinel2Product(
            product_id=product_id,
            acquisition_date=acquisition_date,
            processing_level=processing_level,
            cloud_cover=cloud_cover,
            tile_id=tile_id,
            product_name=product_name,
            metadata=metadata or {},
        )

    def download(
        self,
        product: Sentinel2Product | str,
        destination: str | None = None,
    ) -> ConnectorResult:
        """
        Download a Sentinel-2 product.

        A product ID string is accepted for compatibility with
        the connector API.

        If a downloader has been injected, the request is
        delegated to it. Otherwise the connector reports that
        the product is ready for downloading rather than
        pretending that a file was actually transferred.
        """

        if not product:
            return ConnectorResult.failure(
                provider=self.provider_name,
                operation="download",
                error="Product ID is required",
            )

        product_id = (
            product.product_id
            if isinstance(product, Sentinel2Product)
            else str(product)
        )

        if self.downloader is None:
            return ConnectorResult.ok(
                provider=self.provider_name,
                operation="download",
                data={
                    "status": "download_ready",
                    "product_id": product_id,
                    "destination": destination,
                },
            )

        download_method = getattr(
            self.downloader,
            "download",
            None,
        )

        if download_method is None:
            return ConnectorResult.failure(
                provider=self.provider_name,
                operation="download",
                error=(
                    "Sentinel-2 downloader does not provide "
                    "a download() method."
                ),
            )

        try:
            result = download_method(
                product=product,
                destination=destination,
            )

            return ConnectorResult.ok(
                provider=self.provider_name,
                operation="download",
                data=result,
                metadata={
                    "product_id": product_id,
                    "destination": destination,
                },
            )

        except Exception as exc:
            return ConnectorResult.failure(
                provider=self.provider_name,
                operation="download",
                error=str(exc),
            )

    def connect(self) -> ConnectorResult:
        """
        Validate that the Sentinel-2 connector is configured.
        """

        if self.catalog is None:
            return ConnectorResult.failure(
                provider=self.provider_name,
                operation="connect",
                error="Sentinel-2 catalog is not configured.",
            )

        if self.catalog_service is None:
            return ConnectorResult.failure(
                provider=self.provider_name,
                operation="connect",
                error=(
                    "Sentinel-2 catalog service is not configured."
                ),
            )

        return ConnectorResult.ok(
            provider=self.provider_name,
            operation="connect",
            data={
                "status": "ready",
            },
            metadata={
                "catalog_available": True,
                "catalog_service_available": True,
                "downloader_available": (
                    self.downloader is not None
                ),
            },
        )

    def health_check(self) -> dict[str, Any]:
        """Return the connector health status."""

        connection = self.connect()

        return {
            "provider": self.provider_name,
            "connected": connection.success,
            "catalog_available": self.catalog is not None,
            "catalog_service_available": (
                self.catalog_service is not None
            ),
            "downloader_available": (
                self.downloader is not None
            ),
        }