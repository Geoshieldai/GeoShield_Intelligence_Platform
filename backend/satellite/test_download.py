"""
Tests for the Planet download engine.

Live Planet API tests are disabled by default.
Set RUN_LIVE_SATELLITE_TESTS=1 to enable them.
"""

import asyncio
import os

import pytest

from backend.satellite.planet_download import PlanetDownloadEngine


SCENE_ID = "20200617_204449_0f17"
ASSET_TYPE = "ortho_visual"


RUN_LIVE_TESTS = os.getenv(
    "RUN_LIVE_SATELLITE_TESTS",
    "0",
) == "1"


@pytest.mark.skipif(
    not RUN_LIVE_TESTS,
    reason=(
        "Live Planet satellite tests are disabled. "
        "Set RUN_LIVE_SATELLITE_TESTS=1 to enable them."
    ),
)
def test_planet_download_live() -> None:
    """Test retrieving a Planet scene asset from the live API."""

    async def run() -> object:
        engine = PlanetDownloadEngine()

        return await engine.activate_download(
            SCENE_ID,
            asset_type=ASSET_TYPE,
        )

    asset = asyncio.run(run())

    assert asset is not None