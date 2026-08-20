"""
GeoShield AI Enterprise
Sentinel-2 Downloader

Uses centralized GeoShield configuration.
Credentials are never hard-coded.
"""

from __future__ import annotations

import requests

from core.config import settings


def authenticate() -> str:
    """Authenticate with Copernicus Data Space and return an access token."""

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

    response.raise_for_status()

    payload = response.json()

    access_token = payload.get("access_token")

    if not access_token:
        raise RuntimeError(
            "Copernicus authentication succeeded but no access token was returned."
        )

    return access_token


if __name__ == "__main__":
    token = authenticate()

    print("COPERNICUS AUTHENTICATION: SUCCESS")
    print("Access token received:", bool(token))
    print("Token type: Bearer")
    print("Token stored: NO")
