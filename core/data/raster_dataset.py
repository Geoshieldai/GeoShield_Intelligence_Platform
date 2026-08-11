"""
GeoShield Raster Dataset

Represents raster-based satellite or environmental data.
"""

from dataclasses import dataclass
from typing import Any

from .dataset import GeoDataset


@dataclass
class RasterDataset(GeoDataset):
    """
    Represents a geospatial raster dataset.
    """

    file_path: str | None = None
    bands: list[str] | None = None
    width: int | None = None
    height: int | None = None
    crs: str | None = None
    transform: Any = None

    def to_dict(self) -> dict[str, Any]:
        """Return raster dataset metadata."""

        data = super().to_dict()

        data.update(
            {
                "file_path": self.file_path,
                "bands": self.bands,
                "width": self.width,
                "height": self.height,
                "crs": self.crs,
            }
        )

        return data