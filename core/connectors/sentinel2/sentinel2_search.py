"""
GeoShield Sentinel-2 Search

Provides search filtering for Sentinel-2 products.

This layer is intentionally provider-independent for now.
The live Copernicus connection will be attached later.
"""

from dataclasses import dataclass
from datetime import date


@dataclass
class Sentinel2Search:
    """Sentinel-2 search parameters."""

    start_date: str | None = None
    end_date: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    cloud_cover_max: float = 100.0
    tile_id: str | None = None

    def validate(self) -> bool:
        """Validate search parameters."""

        if not 0 <= self.cloud_cover_max <= 100:
            return False

        if self.latitude is not None:
            if not -90 <= self.latitude <= 90:
                return False

        if self.longitude is not None:
            if not -180 <= self.longitude <= 180:
                return False

        if self.start_date is not None:
            if not self._valid_date(self.start_date):
                return False

        if self.end_date is not None:
            if not self._valid_date(self.end_date):
                return False

        if self.start_date is not None and self.end_date is not None:
            if self.start_date > self.end_date:
                return False

        return True

    @staticmethod
    def _valid_date(value: str) -> bool:
        """Return whether a value is a valid ISO date."""

        try:
            date.fromisoformat(value)
        except (TypeError, ValueError):
            return False

        return True

    def to_dict(self) -> dict[str, object]:
        """Convert search parameters into a dictionary."""

        return {
            "start_date": self.start_date,
            "end_date": self.end_date,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "cloud_cover_max": self.cloud_cover_max,
            "tile_id": self.tile_id,
        }