"""
GeoShield Sentinel-2 Catalog Service

Provides live Sentinel-2 L2A catalog search through the
Copernicus Data Space Sentinel Hub Catalog API.

Responsibilities:
    - Build Catalog search requests.
    - Obtain OAuth access tokens through Sentinel2Auth
      and Sentinel2HTTP.
    - Query the Copernicus Sentinel-2 Catalog API.
    - Apply date and cloud-cover filters.
    - Normalize Catalog items through Sentinel2Catalog.
    - Return consistent Sentinel2Product objects.

This service performs network communication.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any
from wsgiref import headers

import requests

from .sentinel2_auth_adapter import Sentinel2AuthAdapter
from .sentinel2_catalog import Sentinel2Catalog
from .sentinel2_http import Sentinel2HTTP
from .sentinel2_product import Sentinel2Product


class Sentinel2CatalogService:
    """
    Live Sentinel-2 L2A catalog search service.
    """

    CATALOG_SEARCH_URL = (
        "https://sh.dataspace.copernicus.eu/catalog/v1/search"
    )

    COLLECTION = "sentinel-2-l2a"

    def __init__(
        self,
        timeout: float = 30.0,
        catalog: Sentinel2Catalog | None = None,
        auth: Sentinel2AuthAdapter | None = None,
        http: Sentinel2HTTP | None = None,
    ) -> None:
        """
        Initialize the Sentinel-2 catalog service.

        Args:
            timeout:
                HTTP request timeout in seconds.

            catalog:
                Optional catalog normalizer.

            auth:
                Optional Sentinel-2 authentication state.

            http:
                Optional Sentinel-2 HTTP layer.
        """

        self.timeout = timeout
        self.catalog = catalog or Sentinel2Catalog()
        self.auth = auth or Sentinel2AuthAdapter()
        self.http = http or Sentinel2HTTP(
            timeout=int(timeout)
        )

    def search(
        self,
        start_date: str,
        end_date: str,
        cloud_cover_max: float | None = None,
        limit: int = 10,
        bbox: list[float] | None = None,
    ) -> list[Sentinel2Product]:
        """
        Search the live Copernicus Sentinel-2 L2A catalog.

        Args:
            start_date:
                Search start date in YYYY-MM-DD format.

            end_date:
                Search end date in YYYY-MM-DD format.

            cloud_cover_max:
                Optional maximum cloud-cover percentage.

            limit:
                Maximum number of products to return.

            bbox:
                Optional bounding box:
                [west, south, east, north].

        Returns:
            A list of normalized Sentinel2Product objects.

        Raises:
            ValueError:
                If search parameters are invalid.

            RuntimeError:
                If authentication or the Catalog API fails.
        """

        request = self.build_search_request(
            start_date=start_date,
            end_date=end_date,
            cloud_cover_max=cloud_cover_max,
            limit=limit,
            bbox=bbox,
        )

        token = self._get_access_token()

        headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
}

        try:
            response = requests.post(
                request["url"],
                json=request["json"],
                headers=headers,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise RuntimeError(
                "Copernicus Sentinel-2 catalog request failed."
            ) from exc

        if not response.ok:
            raise RuntimeError(
                "Copernicus Sentinel-2 catalog search failed "
                f"(HTTP {response.status_code}). "
                f"{self._safe_error_detail(response)}"
            )

        try:
            payload = response.json()
        except ValueError as exc:
            raise RuntimeError(
                "Invalid Copernicus Catalog response: "
                "response is not valid JSON."
            ) from exc

        features = payload.get("features", [])

        if not isinstance(features, list):
            raise RuntimeError(
                "Invalid Copernicus Catalog response: "
                "'features' must be a list."
            )

        records = [
            self._catalog_item_to_record(item)
            for item in features
            if isinstance(item, dict)
        ]

        return self.catalog.normalize_many(records)

    def build_search_request(
        self,
        start_date: str,
        end_date: str,
        cloud_cover_max: float | None = None,
        limit: int = 10,
        bbox: list[float] | None = None,
    ) -> dict[str, Any]:
        """
        Build a Catalog API search request without sending it.

        Useful for testing and debugging.
        """

        self._validate_dates(start_date, end_date)
        self._validate_limit(limit)

        if cloud_cover_max is not None:
            self._validate_cloud_cover(cloud_cover_max)

        if bbox is not None:
            self._validate_bbox(bbox)

        request: dict[str, Any] = {
            "url": self.CATALOG_SEARCH_URL,
            "method": "POST",
            "json": {
                "collections": [self.COLLECTION],
                "datetime": (
                    f"{start_date}T00:00:00Z/"
                    f"{end_date}T23:59:59Z"
                ),
                "limit": limit,
            },
        }

        if cloud_cover_max is not None:
            request["json"]["filter"] = (
                f"eo:cloud_cover <= {cloud_cover_max}"
            )

        if bbox is not None:
            request["json"]["bbox"] = bbox

        return request

    def _get_access_token(self) -> str:
        """
        Obtain a valid Copernicus access token.

        Supports the central authentication adapter and the
        legacy Sentinel2Auth object used by unit tests.
        """

        try:
            get_token = getattr(self.auth, "get_token", None)

            if callable(get_token):
                return get_token()

            if getattr(self.auth, "token_is_valid", False):
                token = getattr(self.auth, "token", None)
                if token:
                    return token

            client_id = getattr(self.auth, "client_id", None)
            client_secret = getattr(
                self.auth,
                "client_secret",
                None,
            )

            if not client_id or not client_secret:
                raise RuntimeError(
                    "Copernicus authentication credentials are unavailable."
                )

            token_data = self.http.request_token(
                client_id=client_id,
                client_secret=client_secret,
            )

            access_token = token_data.get("access_token")

            if not isinstance(access_token, str) or not access_token:
                raise RuntimeError(
                    "Copernicus authentication response did not contain "
                    "a valid access token."
                )

            set_token = getattr(self.auth, "set_token", None)

            if callable(set_token):
                set_token(
                    access_token,
                    token_data.get("expires_in"),
                )

            return access_token

        except RuntimeError:
            raise

        except Exception as exc:
            raise RuntimeError(
                "Unable to authenticate with Copernicus Data Space."
            ) from exc

    def _catalog_item_to_record(
        self,
        item: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Convert a Sentinel Hub Catalog/STAC Item into the
        internal GeoShield catalog format.
        """

        properties = item.get("properties", {})

        if not isinstance(properties, dict):
            properties = {}

        product_id = item.get("id")

        acquisition_date = (
            properties.get("datetime")
            or properties.get("start_datetime")
            or ""
        )

        processing_level = (
            properties.get("processing:level")
            or properties.get("s2:processing_level")
            or "L2A"
        )

        cloud_cover = properties.get("eo:cloud_cover")

        tile_id = (
            properties.get("s2:mgrs_tile")
            or properties.get("s2:tile")
        )

        product_name = (
            properties.get("title")
            or properties.get("productName")
            or item.get("id")
        )

        return {
            "product_id": product_id,
            "product_name": product_name,
            "acquisition_date": acquisition_date,
            "processing_level": processing_level,
            "cloud_cover": cloud_cover,
            "tile_id": tile_id,
            "geometry": item.get("geometry"),
            "assets": item.get("assets", {}),
            "links": item.get("links", []),
            "metadata": item,
        }

    @staticmethod
    def _validate_dates(
        start_date: str,
        end_date: str,
    ) -> None:
        """
        Validate ISO date strings and date ordering.
        """

        try:
            start = datetime.strptime(
                start_date,
                "%Y-%m-%d",
            )

            end = datetime.strptime(
                end_date,
                "%Y-%m-%d",
            )

        except ValueError as exc:
            raise ValueError(
                "Dates must use YYYY-MM-DD format."
            ) from exc

        if start > end:
            raise ValueError(
                "start_date cannot be later than end_date."
            )

    @staticmethod
    def _validate_limit(limit: int) -> None:
        """
        Validate result limit.
        """

        if not isinstance(limit, int):
            raise ValueError(
                "limit must be an integer."
            )

        if limit < 1:
            raise ValueError(
                "limit must be greater than zero."
            )

        if limit > 100:
            raise ValueError(
                "limit cannot exceed 100."
            )

    @staticmethod
    def _validate_cloud_cover(
        cloud_cover_max: float,
    ) -> None:
        """
        Validate maximum cloud-cover percentage.
        """

        if not 0 <= cloud_cover_max <= 100:
            raise ValueError(
                "cloud_cover_max must be between 0 and 100."
            )

    @staticmethod
    def _validate_bbox(
        bbox: list[float],
    ) -> None:
        """
        Validate a geographic bounding box.
        """

        if len(bbox) != 4:
            raise ValueError(
                "bbox must contain exactly four values: "
                "[west, south, east, north]."
            )

        west, south, east, north = bbox

        if west < -180 or west > 180:
            raise ValueError("Invalid west longitude.")

        if east < -180 or east > 180:
            raise ValueError("Invalid east longitude.")

        if south < -90 or south > 90:
            raise ValueError("Invalid south latitude.")

        if north < -90 or north > 90:
            raise ValueError("Invalid north latitude.")

        if west > east:
            raise ValueError(
                "West longitude cannot exceed east longitude."
            )

        if south > north:
            raise ValueError(
                "South latitude cannot exceed north latitude."
            )

    @staticmethod
    def _safe_error_detail(
        response: requests.Response,
    ) -> str:
        """
        Extract a safe provider error message.

        Credentials and access tokens are never exposed.
        """

        try:
            payload = response.json()

            if isinstance(payload, dict):
                detail = (
                    payload.get("detail")
                    or payload.get("title")
                    or payload.get("message")
                    or payload.get("error")
                )

                if detail:
                    return str(detail)

        except ValueError:
            pass

        text = response.text.strip()

        if text:
            return text[:500]

        return "No additional error information was provided."
