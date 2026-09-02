"""
GeoShield Token Manager

Automatically manages Copernicus OAuth tokens.
"""

from datetime import datetime, timedelta, UTC
from typing import Optional, cast

from satellites.auth.copernicus_auth import CopernicusAuth


class TokenManager:
    """
    Automatically manages Copernicus OAuth tokens.
    """

    def __init__(self):

        self.auth = CopernicusAuth()

        self.token: Optional[str] = None

        self.expiry: Optional[datetime] = None

    def get_token(self) -> str:
        """
        Returns a valid token.
        Automatically refreshes if expired.
        """

        if not self.token_valid():
            return self.refresh_token()

        return cast(str, self.token)

    def refresh_token(self) -> str:
        """
        Requests a fresh OAuth token.
        """

        print("Refreshing Copernicus OAuth Token...")

        self.token = self.auth.authenticate()

        # Token valid for 30 minutes.
        # Refresh after 25 minutes.
        self.expiry = datetime.now(UTC) + timedelta(minutes=25)

        return cast(str, self.token)

    def token_valid(self) -> bool:
        """
        Checks if token is still valid.
        """

        if self.token is None:
            return False

        if self.expiry is None:
            return False

        return datetime.now(UTC) < self.expiry

    def expires_at(self) -> Optional[datetime]:
        """
        Returns token expiry time.
        """

        return self.expiry

    def status(self) -> dict:
        """
        Returns token manager status.
        """

        return {
            "token_loaded": self.token is not None,
            "token_valid": self.token_valid(),
            "expires_at": self.expiry,
        }