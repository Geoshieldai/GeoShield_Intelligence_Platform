"""
GeoShield Data Ingestion

Provides a common interface for bringing external
datasets into the GeoShield data layer.
"""

from typing import Any

from .dataset import GeoDataset


class DataIngestion:
    """
    Basic ingestion service.

    Provider-specific connectors will later use this
    interface to ingest Sentinel, Landsat, VIIRS,
    weather and other datasets.
    """

    def ingest(
        self,
        dataset_id: str,
        source: str,
        product: str,
        data: Any,
        acquisition_date: str | None = None,
    ) -> GeoDataset:
        """
        Convert incoming data into a GeoDataset.
        """

        return GeoDataset(
            dataset_id=dataset_id,
            source=source,
            product=product,
            acquisition_date=acquisition_date,
            metadata={
                "data": data,
            },
        )