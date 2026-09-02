"""
Live Planet search filtering tests.
"""

import pytest

from backend.satellite.planet_search import PlanetSearchEngine


@pytest.mark.live
@pytest.mark.asyncio
async def test_latest_images_respects_cloud_cover_filter():
    """
    Verify that returned scenes satisfy the requested cloud-cover threshold.
    """

    engine = PlanetSearchEngine()

    maximum_cloud_cover = 0.1

    results = await engine.latest_images(
        cloud_cover=maximum_cloud_cover,
        limit=5,
    )

    assert isinstance(results, list)

    for image in results:
        assert image["cloud"] <= maximum_cloud_cover