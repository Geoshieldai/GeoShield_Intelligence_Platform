"""
GeoShield Sentinel-2 Product

Represents a Sentinel-2 satellite product.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Sentinel2Product:
    """Standard representation of a Sentinel-2 product."""

    product_id: str
    acquisition_date: str
    processing_level: str = "L2A"
    cloud_cover: float | None = None
    tile_id: str | None = None
    product_name: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert the product into a dictionary."""

        return {
            "product_id": self.product_id,
            "acquisition_date": self.acquisition_date,
            "processing_level": self.processing_level,
            "cloud_cover": self.cloud_cover,
            "tile_id": self.tile_id,
            "product_name": self.product_name,
            "metadata": self.metadata,
        }