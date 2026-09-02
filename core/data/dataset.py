"""
GeoShield Dataset Model

Defines the common metadata structure for datasets
used throughout the GeoShield platform.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class GeoDataset:
    """
    Represents a geospatial dataset.
    """

    dataset_id: str
    source: str
    product: str
    acquisition_date: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return the dataset as a dictionary."""

        return {
            "dataset_id": self.dataset_id,
            "source": self.source,
            "product": self.product,
            "acquisition_date": self.acquisition_date,
            "metadata": self.metadata,
        }