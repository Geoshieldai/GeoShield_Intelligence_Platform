"""
Pytest tests for Planet SDK authentication.
"""

import os

import pytest
from planet import Auth

from backend.satellite.auth import get_planet_key


@pytest.mark.live
def test_planet_sdk_authentication():
    """
    Verify that the configured Planet API key can create a Planet Auth object.
    """

    key = get_planet_key()

    assert key
    assert len(key) == 36

    auth = Auth.from_key(key)

    assert auth is not None


@pytest.mark.live
def test_planet_api_key_is_not_placeholder():
    """
    Verify that the configured key is not the example placeholder.
    """

    key = os.getenv("PLANET_API_KEY", "").strip()

    assert key
    assert key != "YOUR_REAL_KEY"