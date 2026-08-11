"""
Planet API authentication utilities.
"""

from __future__ import annotations

import os


def get_planet_key() -> str:
    """
    Return the Planet API key from the environment.

    Raises:
        ValueError: If PLANET_API_KEY is not configured.
    """

    key = os.getenv("PLANET_API_KEY", "").strip()

    if not key:
        raise ValueError("Planet API Key not found.")

    return key