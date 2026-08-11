"""
GeoShield Connector Result

Standard result object returned by external data connectors.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ConnectorResult:
    """Standard response from a GeoShield connector."""

    success: bool
    provider: str
    operation: str
    data: Any = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def ok(
        cls,
        provider: str,
        operation: str,
        data: Any = None,
        metadata: dict[str, Any] | None = None,
    ) -> "ConnectorResult":
        """Create a successful result."""

        return cls(
            success=True,
            provider=provider,
            operation=operation,
            data=data,
            metadata=metadata or {},
        )

    @classmethod
    def failure(
        cls,
        provider: str,
        operation: str,
        error: str,
        metadata: dict[str, Any] | None = None,
    ) -> "ConnectorResult":
        """Create a failed result."""

        return cls(
            success=False,
            provider=provider,
            operation=operation,
            error=error,
            metadata=metadata or {},
        )