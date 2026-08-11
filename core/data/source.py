"""
GeoShield Data Source

Defines the standard description of an external data source.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class DataSource:
    """
    Describes an external geospatial or environmental data source.
    """

    source_id: str
    name: str
    provider: str
    source_type: str
    url: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return the source as a dictionary."""

        return {
            "source_id": self.source_id,
            "name": self.name,
            "provider": self.provider,
            "source_type": self.source_type,
            "url": self.url,
            "metadata": self.metadata,
        }