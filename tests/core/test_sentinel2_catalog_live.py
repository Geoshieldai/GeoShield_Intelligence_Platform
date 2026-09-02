
"""
Live integration test for the Sentinel-2 Catalog API.

This test requires valid Copernicus Data Space credentials
in the environment.
"""

from core.connectors.sentinel2.sentinel2_catalog_service import (
    Sentinel2CatalogService,
)


def test_live_sentinel2_catalog_search():
    service = Sentinel2CatalogService(
        timeout=30.0,
    )

    products = service.search(
        start_date="2026-01-01",
        end_date="2026-01-31",
        cloud_cover_max=20.0,
        limit=5,
        bbox=[
            33.9,   # west
            -4.7,   # south
            41.9,   # east
            5.1,    # north
        ],
    )

    assert isinstance(products, list)