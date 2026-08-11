"""
GeoShield Sentinel-2 Authentication

Handles Copernicus Data Space credentials and OAuth2 token state.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass
class Sentinel2Auth:
    """
    Sentinel-2 authentication configuration and token state.
    """

    client_id: str | None = None
    client_secret: str | None = None
    token: str | None = None
    expires_at: float | None = None

    def __post_init__(self) -> None:
        """Load credentials from environment when not supplied."""

        if self.client_id is None:
            self.client_id = os.getenv("COPERNICUS_CLIENT_ID")

        if self.client_secret is None:
            self.client_secret = os.getenv(
                "COPERNICUS_CLIENT_SECRET"
            )

    @property
    def is_configured(self) -> bool:
        """Return True when both client credentials exist."""

        return bool(
            self.client_id
            and self.client_secret
        )

    @property
    def has_token(self) -> bool:
        """Return True when an access token exists."""

        return bool(self.token)

    @property
    def token_is_valid(self) -> bool:
        """Return True when the stored token is still valid."""

        if not self.token:
            return False

        if self.expires_at is None:
            return True

        return time.time() < self.expires_at

    def set_token(
        self,
        token: str,
        expires_in: int | float | str | None = None,
    ) -> None:
        """
        Store an access token and calculate its expiration time.
        """

        if not token:
            raise ValueError(
                "Access token cannot be empty."
            )

        self.token = token

        if expires_in is None:
            self.expires_at = None
            return

        try:
            seconds = float(expires_in)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                "expires_in must be numeric."
            ) from exc

        self.expires_at = time.time() + seconds

    def clear_token(self) -> None:
        """Clear the stored access token."""

        self.token = None
        self.expires_at = None

    def validate(self) -> bool:
        """
        Return True when authentication is ready.

        Valid credentials or a valid existing token are accepted.
        """

        return self.is_configured or self.token_is_valid

    def to_dict(self) -> dict[str, object]:
        """
        Return safe authentication information.

        Credentials, secrets, and tokens are never returned.
        """

        return {
            "configured": self.is_configured,
            "has_token": self.has_token,
            "token_is_valid": self.token_is_valid,
        }