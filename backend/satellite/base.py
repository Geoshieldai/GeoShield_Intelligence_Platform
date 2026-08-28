"""
GeoShield AI Enterprise
Common satellite interface.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SatelliteDefinition:
    id: str
    name: str
    provider: str
    category: str
    status: str = "integrating"
    description: str = ""
    capabilities: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class SatelliteBase:
    """Base interface for GeoShield satellite engines."""

    name = "Unknown Satellite"
    satellite_id = "unknown"

    def status(self) -> str:
        return "integrating"

    def capabilities(self) -> list[str]:
        return []

    def latest(self) -> dict[str, Any]:
        return {
            "status": "unavailable",
            "message": "Latest imagery/data is not implemented yet.",
        }
