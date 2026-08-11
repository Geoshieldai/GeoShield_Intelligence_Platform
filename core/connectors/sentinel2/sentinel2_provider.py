"""
GeoShield Sentinel-2 Provider

Defines the provider abstraction used by the Sentinel-2
integration layer.

This module does not perform network communication yet.
It establishes a clean provider contract that can later
be connected to Copernicus Data Space or another supported
Sentinel-2 provider.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Sentinel2Provider:
    """
    Provider definition for Sentinel-2 data.

    The provider stores connection information and exposes
    metadata describing the provider.
    """

    name: str = "Copernicus Data Space"
    base_url: str = "https://dataspace.copernicus.eu"
    collection: str = "SENTINEL-2"
    enabled: bool = True

    @property
    def provider_name(self) -> str:
        """Return the provider name."""

        return self.name

    def is_available(self) -> bool:
        """
        Return whether the provider is enabled.

        Network availability will be checked later by the
        live provider client.
        """

        return self.enabled

    def describe(self) -> dict[str, Any]:
        """
        Return provider metadata.
        """

        return {
            "name": self.name,
            "base_url": self.base_url,
            "collection": self.collection,
            "enabled": self.enabled,
        }