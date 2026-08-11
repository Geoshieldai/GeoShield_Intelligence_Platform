"""
GeoShield Data Connectors

Standard interfaces and utilities for connecting GeoShield
to satellite, weather, environmental, and other external
data providers.
"""

from .base_connector import BaseConnector
from .connector_config import ConnectorConfig
from .connector_registry import ConnectorRegistry
from .connector_result import ConnectorResult

__all__ = [
    "BaseConnector",
    "ConnectorConfig",
    "ConnectorRegistry",
    "ConnectorResult",
]