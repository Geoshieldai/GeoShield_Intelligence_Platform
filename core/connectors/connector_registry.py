"""
GeoShield Connector Registry

Maintains all available external data connectors.
"""

from .base_connector import BaseConnector


class ConnectorRegistry:
    """
    Registry for GeoShield data connectors.
    """

    def __init__(self) -> None:
        self._connectors: dict[str, BaseConnector] = {}

    def register(self, connector: BaseConnector) -> None:
        """Register a connector."""

        self._connectors[connector.provider_name] = connector

    def get(self, provider_name: str) -> BaseConnector | None:
        """Retrieve a connector by provider name."""

        return self._connectors.get(provider_name)

    def list(self) -> list[BaseConnector]:
        """Return all registered connectors."""

        return list(self._connectors.values())

    def count(self) -> int:
        """Return the number of registered connectors."""

        return len(self._connectors)

    def remove(self, provider_name: str) -> bool:
        """Remove a connector from the registry."""

        if provider_name not in self._connectors:
            return False

        del self._connectors[provider_name]
        return True

    def clear(self) -> None:
        """Remove all registered connectors."""

        self._connectors.clear()