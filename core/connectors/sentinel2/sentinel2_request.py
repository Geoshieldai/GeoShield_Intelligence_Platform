"""
GeoShield Sentinel-2 Search Request

Defines the normalized search request sent from GeoShield
toward the Sentinel-2 provider layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Sentinel2Request:
    """
    Normalized Sentinel-2 search request.
    """

    start_date: str
    end_date: str
    cloud_cover_max: float | None = None
    collection: str = "SENTINEL-2"
    tile_id: str | None = None
    bbox: tuple[float, float, float, float] | None = None

    def validate(self) -> bool:
        """
        Validate the search request.
        """

        if not self.start_date:
            return False

        if not self.end_date:
            return False

        if self.cloud_cover_max is not None:
            if not 0 <= self.cloud_cover_max <= 100:
                return False

        if self.bbox is not None:
            if len(self.bbox) != 4:
                return False

            min_lon, min_lat, max_lon, max_lat = self.bbox

            if min_lon > max_lon:
                return False

            if min_lat > max_lat:
                return False

            if not -180 <= min_lon <= 180:
                return False

            if not -180 <= max_lon <= 180:
                return False

            if not -90 <= min_lat <= 90:
                return False

            if not -90 <= max_lat <= 90:
                return False

        return True

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the request into a provider-ready dictionary.
        """

        return {
            "collection": self.collection,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "cloud_cover_max": self.cloud_cover_max,
            "tile_id": self.tile_id,
            "bbox": self.bbox,
        }