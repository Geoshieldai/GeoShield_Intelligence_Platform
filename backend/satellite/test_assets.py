"""
Live Planet asset tests.
"""

import pytest

from backend.satellite.planet_assets import PlanetAssetEngine


SCENE_ID = "20260726_170618_52_24d8"


@pytest.mark.live
@pytest.mark.asyncio
async def test_planet_asset_engine_initializes():
    """
    Verify that the Planet asset engine can initialize with the configured key.
    """

    engine = PlanetAssetEngine()

    assert engine is not None
    assert engine.auth is not None


@pytest.mark.live
@pytest.mark.asyncio
async def test_planet_scene_has_ortho_visual_asset():
    """
    Verify that the scene exposes the ortho_visual asset.
    """

    engine = PlanetAssetEngine()

    asset = await engine.get_asset(
        SCENE_ID,
        "ortho_visual",
    )

    assert asset == "ortho_visual"