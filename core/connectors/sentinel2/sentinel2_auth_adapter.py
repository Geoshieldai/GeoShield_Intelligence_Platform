"""
GeoShield Sentinel-2 Authentication Adapter

Bridges the Sentinel-2 connector to the central
GeoShield Copernicus authentication manager.
"""

from __future__ import annotations

from core.auth.copernicus import CopernicusAuthManager
from core.auth.exceptions import (
    CopernicusAuthenticationError,
    CopernicusConfigurationError,
    CopernicusNetworkError,
)


class Sentinel2AuthAdapter:
    """
    Authentication adapter for Sentinel-2.

    Uses the central GeoShield CopernicusAuthManager
    instead of maintaining a second credential system.
    """

    def __init__(
        self,
        auth_manager: CopernicusAuthManager | None = None,
    ) -> None:
        self.auth_manager = (
            auth_manager
            if auth_manager is not None
            else CopernicusAuthManager()
        )

    @property
    def is_configured(self) -> bool:
        """
        Return whether the central Copernicus credentials
        are configured.
        """

        from core.config import settings

        return bool(
            settings.cdse_username
            and settings.cdse_password
            and settings.cdse_client_id
            and settings.cdse_token_url
        )

    @property
    def has_token(self) -> bool:
        """Return whether a valid token is currently cached."""

        return self.auth_manager.is_token_valid()

    @property
    def token(self) -> str | None:
        """Return the cached token when it is still valid."""

        if not self.auth_manager.is_token_valid():
            return None

        return self.auth_manager.state.access_token

    def get_token(self) -> str:
        """Return a valid Copernicus access token."""

        return self.auth_manager.get_token()

    def authenticate(self) -> dict[str, object]:
        """
        Authenticate through the central Copernicus
        authentication manager.
        """

        token = self.auth_manager.get_token()

        return {
            "authenticated": bool(token),
            "token_available": bool(token),
            "seconds_remaining": round(
                self.auth_manager.seconds_remaining(),
                1,
            ),
        }

    def validate(self) -> bool:
        """
        Return whether the central Copernicus configuration
        is available.
        """

        return self.is_configured

    def clear_token(self) -> None:
        """Clear the cached Copernicus token."""

        self.auth_manager.state.access_token = None
        self.auth_manager.state.expires_at = 0.0

    def to_dict(self) -> dict[str, bool]:
        """Return safe authentication status information."""

        return {
            "configured": self.is_configured,
            "has_token": self.has_token,
            "token_is_valid": self.has_token,
        }
