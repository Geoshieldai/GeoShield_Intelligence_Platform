"""
Live PlanetService integration tests.
"""

import pytest

from backend.satellite.planet_service import PlanetService


@pytest.mark.live
@pytest.mark.asyncio
async def test_planet_service_initializes():
    """
    Verify that PlanetService can initialize successfully.
    """

    service = PlanetService()

    assert service is not None
    assert service.search_engine is not None
    assert service.asset_engine is not None


@pytest.mark.live
@pytest.mark.asyncio
async def test_latest_scene_assets_returns_expected_structure():
    """
    Verify the latest_scene_assets service contract.
    """

    service = PlanetService()

    result = await service.latest_scene_assets()

    if result is None:
        pytest.skip("Planet returned no scenes matching the current filter.")

    assert "scene" in result
    assert "assets" in result

    assert result["scene"] is not None
    assert isinstance(result["assets"], list)