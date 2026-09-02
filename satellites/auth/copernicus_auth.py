"""
Copernicus OAuth Authentication
"""

from typing import Optional, cast

import requests

from core.config import (
    COPERNICUS_CLIENT_ID,
    COPERNICUS_CLIENT_SECRET,
    TOKEN_URL,
)


class CopernicusAuth:
    """
    Handles OAuth authentication with Copernicus Data Space Ecosystem.
    """

    def __init__(self):

        self.token: Optional[str] = None

    def authenticate(self) -> str:

        client_id = cast(str, COPERNICUS_CLIENT_ID)
        client_secret = cast(str, COPERNICUS_CLIENT_SECRET)

        print()
        print("========== Copernicus Authentication ==========")
        print("Token URL:", TOKEN_URL)
        print("Client ID Loaded:", bool(client_id))
        print("Client Secret Loaded:", bool(client_secret))
        print("Client Secret Length:", len(client_secret))
        print("===============================================")
        print()

        response = requests.post(
            TOKEN_URL,
            data={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
            },
        )

        print("HTTP Status :", response.status_code)
        print("Server Reply:", response.text)
        print()

        response.raise_for_status()

        self.token = response.json()["access_token"]

        print("Authentication Successful.")
        print()

        return cast(str, self.token)