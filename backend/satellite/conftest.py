"""
Pytest configuration for Planet satellite integration tests.
"""

import os

import pytest


def pytest_collection_modifyitems(config, items):
    """
    Skip Planet live integration tests when PLANET_API_KEY is unavailable.
    """

    planet_key = os.getenv("PLANET_API_KEY", "").strip()

    if planet_key:
        return

    skip_marker = pytest.mark.skip(
        reason="PLANET_API_KEY is not configured."
    )

    for item in items:
        path = str(item.fspath).replace("\\", "/")

        if "/backend/satellite/" in path and (
            "test_asset" in path
            or "test_latest" in path
            or "test_search" in path
            or "test_service" in path
            or "test_permissions" in path
            or "test_sdk" in path
            or "test_manager" in path
        ):
            item.add_marker(skip_marker)