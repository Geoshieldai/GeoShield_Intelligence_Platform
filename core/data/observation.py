"""
GeoShield Observation Model

Represents an individual environmental or satellite observation.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Observation:
    """
    Represents one geospatial observation.
    """

    observation_id: str
    latitude: float
    longitude: float
    timestamp: str
    source: str
    values: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return the observation as a dictionary."""

        return {
            "observation_id": self.observation_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timestamp": self.timestamp,
            "source": self.source,
            "values": self.values,
        }