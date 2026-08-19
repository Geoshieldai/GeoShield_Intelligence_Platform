"""
GeoShield AI Enterprise
Planet Authentication Manager

Centralized access to Planet API credentials.

Credentials are loaded exclusively through
GeoShield's central configuration layer.
"""

from __future__ import annotations

from core.config import settings


class PlanetConfigurationError(RuntimeError):
    """Raised when Planet configuration is missing or invalid."""


class PlanetAuthManager:
    """Manage Planet API authentication credentials."""

    def __init__(self) -> None:
        """Initialize the Planet authentication manager."""
        self._validate_configuration()

    def _validate_configuration(self) -> None:
        """Validate that the Planet API key is configured."""

        if not settings.planet_api_key:
            raise PlanetConfigurationError(
                "Planet API key is not configured."
            )

    def get_api_key(self) -> str:
        """
        Return the configured Planet API key.

        The key is never printed or logged by this manager.
        """

        return settings.planet_api_key


__all__ = [
    "PlanetAuthManager",
    "PlanetConfigurationError",
]