"""
GeoShield Data Registry

Maintains registered data sources and provides lookup
functionality for the ingestion layer.
"""

from .source import DataSource


class DataSourceRegistry:
    """
    Registry of external GeoShield data sources.
    """

    def __init__(self) -> None:
        self._sources: dict[str, DataSource] = {}

    def register(self, source: DataSource) -> None:
        """Register a data source."""

        self._sources[source.source_id] = source

    def get(self, source_id: str) -> DataSource | None:
        """Retrieve a registered source."""

        return self._sources.get(source_id)

    def list(self) -> list[DataSource]:
        """Return all registered sources."""

        return list(self._sources.values())

    def count(self) -> int:
        """Return the number of registered sources."""

        return len(self._sources)