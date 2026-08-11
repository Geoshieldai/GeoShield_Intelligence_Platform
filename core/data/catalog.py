"""
GeoShield Dataset Catalog

Stores and retrieves datasets known to the GeoShield system.
"""

from .dataset import GeoDataset


class DatasetCatalog:
    """
    In-memory catalog of GeoShield datasets.

    Later this can be connected to PostGIS,
    STAC catalogs, cloud storage and satellite APIs.
    """

    def __init__(self) -> None:
        self._datasets: dict[str, GeoDataset] = {}

    def register(self, dataset: GeoDataset) -> None:
        """Register a dataset."""

        self._datasets[dataset.dataset_id] = dataset

    def get(self, dataset_id: str) -> GeoDataset | None:
        """Retrieve a dataset by ID."""

        return self._datasets.get(dataset_id)

    def list(self) -> list[GeoDataset]:
        """Return all registered datasets."""

        return list(self._datasets.values())

    def count(self) -> int:
        """Return the number of registered datasets."""

        return len(self._datasets)