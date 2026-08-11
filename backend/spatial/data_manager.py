"""
GeoShield Spatial Data Manager

Manages loading and retrieval of geospatial data layers.
"""

from __future__ import annotations

from pathlib import Path

import geopandas as gpd


class GeoDataManager:
    """Manage GeoPandas-based spatial data layers."""

    def __init__(self) -> None:
        """Initialize the spatial data manager."""

        self.layers: dict[str, gpd.GeoDataFrame] = {}

    def load_layer(
        self,
        name: str,
        filepath: str,
    ) -> None:
        """
        Load a geospatial layer.

        Args:
            name: Internal name used to identify the layer.
            filepath: Path to the geospatial dataset.

        Raises:
            FileNotFoundError: If the dataset does not exist.
            ValueError: If the layer name is empty.
        """

        if not name.strip():
            raise ValueError("Layer name is required.")

        path = Path(filepath)

        if not path.exists():
            raise FileNotFoundError(
                f"Spatial dataset not found: {path}"
            )

        layer = gpd.read_file(path)

        self.layers[name] = layer

        print(
            f"Spatial layer '{name}' loaded successfully."
        )

    def get_layer(
        self,
        name: str,
    ) -> gpd.GeoDataFrame | None:
        """
        Retrieve a loaded spatial layer.

        Args:
            name: Layer name.

        Returns:
            The GeoDataFrame if loaded, otherwise None.
        """

        return self.layers.get(name)

    def list_layers(self) -> list[str]:
        """
        Return the names of all loaded layers.
        """

        return list(self.layers.keys())