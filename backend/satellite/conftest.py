"""
Pytest configuration for GeoShield satellite tests.
"""

from pathlib import Path
import os

import pytest
from dotenv import load_dotenv


# Project root:
# G:\My Drive\GeoShield_Project
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Load the local .env file into the pytest process.
load_dotenv(PROJECT_ROOT / ".env")


def pytest_collection_modifyitems(config, items):
    """
    Skip live Planet integration tests when PLANET_API_KEY is unavailable.
    """

    planet_key = os.getenv("PLANET_API_KEY", "").strip()

    if planet_key:
        return

    skip_live = pytest.mark.skip(
        reason="PLANET_API_KEY is not configured."
    )

    for item in items:
        if "live" in item.keywords:
            item.add_marker(skip_live)