"""
GeoShield Environmental Context

Stores the environmental intelligence produced by the
GeoShield environmental analysis pipeline.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class EnvironmentalContext:
    """
    Structured environmental context passed through the GeoShield kernel.
    """

    indices: dict[str, float] = field(default_factory=dict)
    classifications: dict[str, str] = field(default_factory=dict)
    environmental_score: float = 0.0
    condition: str = ""
    risk_level: str = ""
    report: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the environmental context into a dictionary.
        """

        return {
            "indices": self.indices,
            "classifications": self.classifications,
            "environmental_score": self.environmental_score,
            "condition": self.condition,
            "risk_level": self.risk_level,
            "report": self.report,
        }