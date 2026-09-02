"""
GeoShield Sentinel-2 Metadata

Provides a normalized representation of metadata associated
with a Sentinel-2 satellite product.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Sentinel2Metadata:
    """
    Standardized Sentinel-2 product metadata.
    """

    product_id: str
    acquisition_date: str
    tile_id: str | None = None
    cloud_cover: float | None = None
    processing_level: str | None = None
    platform: str = "Sentinel-2"
    instrument: str = "MSI"
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """
        Validate the metadata.
        """

        if not self.product_id:
            return False

        if not self.acquisition_date:
            return False

        if self.cloud_cover is not None:
            if not 0 <= self.cloud_cover <= 100:
                return False

        return True

    def to_dict(self) -> dict[str, Any]:
        """
        Convert metadata into a dictionary.
        """

        return {
            "product_id": self.product_id,
            "acquisition_date": self.acquisition_date,
            "tile_id": self.tile_id,
            "cloud_cover": self.cloud_cover,
            "processing_level": self.processing_level,
            "platform": self.platform,
            "instrument": self.instrument,
            "metadata": self.metadata,
        }