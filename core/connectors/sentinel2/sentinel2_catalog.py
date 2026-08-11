"""
GeoShield Sentinel-2 Catalog

Provides catalog-result normalization for Sentinel-2 products.

This layer does not perform network communication. It converts
provider responses into a consistent GeoShield representation.
"""

from __future__ import annotations

from typing import Any

from .sentinel2_product import Sentinel2Product


class Sentinel2Catalog:
    """Normalize Sentinel-2 catalog records."""

    def normalize_product(
        self,
        record: dict[str, Any],
    ) -> Sentinel2Product:
        """
        Convert a provider catalog record into a Sentinel2Product.

        Args:
            record: Raw Sentinel-2 catalog record.

        Returns:
            A normalized Sentinel2Product object.

        Raises:
            ValueError: If the record does not contain a product ID.
        """

        product_id = (
            record.get("product_id")
            or record.get("id")
            or record.get("identifier")
        )

        if not product_id:
            raise ValueError(
                "Sentinel-2 product ID is required."
            )

        acquisition_date = (
            record.get("acquisition_date")
            or record.get("date")
            or record.get("datetime")
            or ""
        )

        processing_level = (
            record.get("processing_level")
            or record.get("processingLevel")
            or "L2A"
        )

        cloud_cover = record.get("cloud_cover")

        if cloud_cover is None:
            cloud_cover = record.get("cloudCover")

        tile_id = (
            record.get("tile_id")
            or record.get("tileId")
        )

        product_name = (
            record.get("product_name")
            or record.get("productName")
            or record.get("name")
        )

        return Sentinel2Product(
            product_id=str(product_id),
            acquisition_date=str(acquisition_date),
            processing_level=str(processing_level),
            cloud_cover=cloud_cover,
            tile_id=tile_id,
            product_name=product_name,
            metadata=dict(record),
        )

    def normalize_many(
        self,
        records: list[dict[str, Any]],
    ) -> list[Sentinel2Product]:
        """
        Normalize multiple catalog records.

        Args:
            records: A list of raw Sentinel-2 catalog records.

        Returns:
            A list of normalized Sentinel2Product objects.
        """

        return [
            self.normalize_product(record)
            for record in records
        ]