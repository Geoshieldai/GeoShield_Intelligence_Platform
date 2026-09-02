"""
GeoShield Base Connector

Defines the standard interface that every external
data provider connector must follow.
"""

from abc import ABC, abstractmethod
from typing import Any

from .connector_config import ConnectorConfig
from .connector_result import ConnectorResult


class BaseConnector(ABC):
    """
    Base class for all GeoShield external data connectors.

    Future connectors such as Sentinel-1, Sentinel-2,
    Landsat, VIIRS, GPM, and weather providers will
    implement this interface.
    """

    def __init__(self, config: ConnectorConfig) -> None:
        """Initialize the connector with its configuration."""

        self.config = config

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the provider name."""

    @abstractmethod
    def connect(self) -> ConnectorResult:
        """Establish a connection to the external provider."""

    @abstractmethod
    def search(
        self,
        **filters: Any,
    ) -> ConnectorResult:
        """Search the provider for available data."""

    @abstractmethod
    def download(
        self,
        product_id: str,
    ) -> ConnectorResult:
        """Download a specific product or dataset."""

    def is_enabled(self) -> bool:
        """Return whether the connector is enabled."""

        return self.config.enabled