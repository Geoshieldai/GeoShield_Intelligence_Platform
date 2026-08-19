"""
Planet API authentication utilities.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


# Project root:
# G:\My Drive\GeoShield_Project
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Load the local .env file if it exists.
ENV_FILE = PROJECT_ROOT / ".env"
load_dotenv(ENV_FILE)


def get_planet_key() -> str:
    """
    Return the Planet API key from the environment or local .env file.

    Raises:
        ValueError: If PLANET_API_KEY is not configured.
    """

    key = os.getenv("PLANET_API_KEY", "").strip()

    if not key:
        raise ValueError(
            "Planet API Key not found. "
            f"Expected PLANET_API_KEY in environment or {ENV_FILE}"
        )

    return key