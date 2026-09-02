"""
Live SatelliteManager integration tests.
"""

import pytest

from backend.satellite.satellite_manager import SatelliteManager


@pytest.mark.live
@pytest.mark.asyncio
async def test_satellite_manager_initializes():
    """
    Verify that SatelliteManager registers the Planet provider.
    """

    manager = SatelliteManager()

    assert manager is not None
    assert "planet" in manager.providers


@pytest.mark.live
@pytest.mark.asyncio
async def test_satellite_manager_planet_provider_returns_images():
    """
    Verify that the Planet provider is reachable through SatelliteManager.
    """

    manager = SatelliteManager()

    planet_provider = manager.provider("planet")

    assert planet_provider is not None

    scenes = await planet_provider.latest_images(limit=3)

    assert isinstance(scenes, list)