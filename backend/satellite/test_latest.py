"""
Live Planet search tests.
"""

import pytest

from backend.satellite.planet_search import PlanetSearchEngine


@pytest.mark.live
@pytest.mark.asyncio
async def test_latest_images_returns_scene_records():
    """
    Verify that PlanetSearchEngine can retrieve recent Planet scenes.
    """

    engine = PlanetSearchEngine()

    images = await engine.latest_images(limit=5)

    assert isinstance(images, list)

    for image in images:
        assert "id" in image
        assert "published" in image
        assert "stage" in image
        assert "quality" in image
        assert "cloud" in image