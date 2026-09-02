"""
GeoShield Sentinel-2 Live Integration Status

Describes whether the Sentinel-2 connector is operating in
architecture-only mode or live-provider mode.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Sentinel2LiveStatus:
    """
    Sentinel-2 integration status.
    """

    enabled: bool = False
    authenticated: bool = False
    network_enabled: bool = False

    @property
    def is_live(self) -> bool:
        """
        Return True only when all live integration requirements
        are enabled.
        """
        return (
            self.enabled
            and self.authenticated
            and self.network_enabled
        )

    def to_dict(self) -> dict[str, bool]:
        """
        Convert status to a dictionary.
        """
        return {
            "enabled": self.enabled,
            "authenticated": self.authenticated,
            "network_enabled": self.network_enabled,
            "is_live": self.is_live,
        }