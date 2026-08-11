"""
GeoShield Sentinel-2 Endpoint Configuration

Defines the provider endpoints used by the Sentinel-2
integration layer.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Sentinel2Endpoint:
    """
    Sentinel-2 provider endpoint configuration.
    """

    base_url: str = "https://catalogue.dataspace.copernicus.eu"
    search_path: str = "/resto/api/collections/Sentinel2"
    token_url: str = (
        "https://identity.dataspace.copernicus.eu/auth/realms/"
        "CDSE/protocol/openid-connect/token"
    )

    @property
    def search_url(self) -> str:
        """
        Return the complete catalog search URL.
        """
        return f"{self.base_url}{self.search_path}"

    def to_dict(self) -> dict[str, str]:
        """
        Return endpoint configuration as a dictionary.
        """
        return {
            "base_url": self.base_url,
            "search_path": self.search_path,
            "search_url": self.search_url,
            "token_url": self.token_url,
        }