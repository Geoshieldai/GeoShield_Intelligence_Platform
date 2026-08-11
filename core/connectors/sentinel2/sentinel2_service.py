"""
GeoShield Sentinel-2 Service

Application-level service for Sentinel-2 catalog operations.
"""

from __future__ import annotations

from typing import Any

from .sentinel2_catalog import Sentinel2Catalog
from .sentinel2_product_parser import Sentinel2ProductParser
from .sentinel2_query import Sentinel2Query
from .sentinel2_request import Sentinel2Request


class Sentinel2Service:
    """
    Coordinate Sentinel-2 query, parsing and catalog normalization.
    """

    def __init__(
        self,
        catalog: Sentinel2Catalog | None = None,
        parser: Sentinel2ProductParser | None = None,
    ) -> None:
        self.catalog = catalog or Sentinel2Catalog()
        self.parser = parser or Sentinel2ProductParser()

    def build_query(
        self,
        request: Sentinel2Request,
    ) -> dict[str, Any]:
        """
        Build provider query parameters.
        """

        return Sentinel2Query(request).to_params()

    def parse_product(
        self,
        record: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Parse a raw provider record.
        """

        return self.parser.parse(record)

    def normalize_product(
        self,
        record: dict[str, Any],
    ):
        """
        Convert a provider record into a Sentinel2Product.
        """

        return self.catalog.normalize_product(record)

    def normalize_products(
        self,
        records: list[dict[str, Any]],
    ):
        """
        Normalize multiple provider records.
        """

        return self.catalog.normalize_many(records)