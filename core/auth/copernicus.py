"""
GeoShield AI Enterprise
Copernicus Authentication Manager
"""

from __future__ import annotations

import time
from dataclasses import dataclass

import requests

from core.config import settings
from core.auth.exceptions import (
    CopernicusAuthenticationError,
    CopernicusConfigurationError,
    CopernicusNetworkError,
)


@dataclass
class TokenState:
    """Runtime state of a Copernicus access token."""

    access_token: str | None = None
    expires_at: float = 0.0


class CopernicusAuthManager:
    """Manage Copernicus authentication and token lifecycle."""

    def __init__(self, max_retries: int = 2) -> None:
        self.state = TokenState()
        self.max_retries = max(0, max_retries)

    def is_token_valid(self) -> bool:
        """Return True when a usable token is currently cached."""

        return (
            self.state.access_token is not None
            and time.time() < self.state.expires_at
        )

    def seconds_remaining(self) -> float:
        """Return remaining lifetime of the cached token."""

        if not self.is_token_valid():
            return 0.0

        return max(
            self.state.expires_at - time.time(),
            0.0,
        )

    def _validate_configuration(self) -> None:
        """Validate required Copernicus configuration."""

        if not settings.cdse_username:
            raise CopernicusConfigurationError(
                "CDSE username is not configured."
            )

        if not settings.cdse_password:
            raise CopernicusConfigurationError(
                "CDSE password is not configured."
            )

        if not settings.cdse_client_id:
            raise CopernicusConfigurationError(
                "CDSE client ID is not configured."
            )

    def authenticate(self) -> str:
        """Authenticate against Copernicus."""

        self._validate_configuration()

        attempts = self.max_retries + 1

        for attempt in range(1, attempts + 1):

            try:
                response = requests.post(
                    settings.cdse_token_url,
                    data={
                        "grant_type": "password",
                        "client_id": settings.cdse_client_id,
                        "username": settings.cdse_username,
                        "password": settings.cdse_password,
                    },
                    timeout=settings.http_timeout,
                )

            except requests.RequestException as exc:

                if attempt >= attempts:
                    raise CopernicusNetworkError(
                        "Unable to reach Copernicus authentication service."
                    ) from exc

                time.sleep(1)

                continue

            if response.status_code in (400, 401, 403):
                raise CopernicusAuthenticationError(
                    "Copernicus rejected the authentication request."
                )

            try:
                response.raise_for_status()
            except requests.RequestException as exc:
                if attempt >= attempts:
                    raise CopernicusNetworkError(
                        "Copernicus authentication request failed."
                    ) from exc

                time.sleep(1)

                continue

            try:
                payload = response.json()
            except ValueError as exc:
                raise CopernicusAuthenticationError(
                    "Copernicus returned an invalid authentication response."
                ) from exc

            token = payload.get("access_token")
            expires_in = payload.get("expires_in", 1800)

            if not token:
                raise CopernicusAuthenticationError(
                    "Copernicus returned no access token."
                )

            safety_margin = 60

            self.state.access_token = token

            self.state.expires_at = (
                time.time()
                + max(int(expires_in) - safety_margin, 1)
            )

            return token

        raise CopernicusNetworkError(
            "Authentication failed after retry attempts."
        )

    def get_token(self) -> str:
        """Return cached token or authenticate when necessary."""

        if not self.is_token_valid():
            return self.authenticate()

        return self.state.access_token
