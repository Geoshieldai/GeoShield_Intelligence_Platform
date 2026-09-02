"""
GeoShield Sentinel-2 Product Parser

Extracts useful information from Sentinel-2 provider records.
"""

from __future__ import annotations

from typing import Any


class Sentinel2ProductParser:
    """
    Parse Sentinel-2 product metadata.
    """

    def extract_product_id(
        self,
        record: dict[str, Any],
    ) -> str | None:
        """
        Extract a Sentinel-2 product identifier.
        """

        value = (
            record.get("product_id")
            or record.get("id")
            or record.get("identifier")
        )

        return str(value) if value else None

    def extract_acquisition_date(
        self,
        record: dict[str, Any],
    ) -> str | None:
        """
        Extract the acquisition datetime/date.
        """

        value = (
            record.get("acquisition_date")
            or record.get("datetime")
            or record.get("date")
        )

        return str(value) if value else None

    def extract_cloud_cover(
        self,
        record: dict[str, Any],
    ) -> float | None:
        """
        Extract cloud-cover percentage.
        """

        value = (
            record.get("cloud_cover")
            if record.get("cloud_cover") is not None
            else record.get("cloudCover")
        )

        if value is None:
            return None

        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def extract_tile_id(
        self,
        record: dict[str, Any],
    ) -> str | None:
        """
        Extract Sentinel-2 tile identifier.
        """

        value = (
            record.get("tile_id")
            or record.get("tileId")
        )

        return str(value) if value else None

    def parse(
        self,
        record: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Parse a provider record into a standardized dictionary.
        """

        return {
            "product_id": self.extract_product_id(record),
            "acquisition_date": self.extract_acquisition_date(record),
            "cloud_cover": self.extract_cloud_cover(record),
            "tile_id": self.extract_tile_id(record),
        }