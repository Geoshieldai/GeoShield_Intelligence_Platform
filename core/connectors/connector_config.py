"""
GeoShield Connector Configuration

Stores configuration shared by external data connectors.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ConnectorConfig:
    """Configuration for an external GeoShield connector."""

    connector_id: str
    provider: str
    enabled: bool = True
    base_url: str | None = None
    timeout: float = 30.0
    retries: int = 3
    credentials: dict[str, Any] = field(default_factory=dict)
    options: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate basic connector configuration."""

        if not self.connector_id:
            return False

        if not self.provider:
            return False

        if self.timeout <= 0:
            return False

        if self.retries < 0:
            return False

        return True