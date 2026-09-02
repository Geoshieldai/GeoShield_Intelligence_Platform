"""
Tests for the GeoShield river spatial-data layer.
"""

from pathlib import Path

import pytest

from backend.spatial.data_manager import GeoDataManager


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RIVERS_FILE = PROJECT_ROOT / "data" / "rivers" / "kenya_rivers.shp"


@pytest.mark.skipif(
    not RIVERS_FILE.exists(),
    reason=(
        "Kenya rivers shapefile is not available yet: "
        f"{RIVERS_FILE}"
    ),
)
def test_river_layer_can_be_loaded() -> None:
    """The Kenya rivers layer should load when the dataset exists."""

    manager = GeoDataManager()

    manager.load_layer(
        "rivers",
        str(RIVERS_FILE),
    )

    rivers = manager.get_layer("rivers")

    assert rivers is not None
    assert len(rivers) >= 0


@pytest.mark.skipif(
    not RIVERS_FILE.exists(),
    reason=(
        "Kenya rivers shapefile is not available yet: "
        f"{RIVERS_FILE}"
    ),
)
def test_river_layer_is_registered() -> None:
    """The rivers layer should be registered after loading."""

    manager = GeoDataManager()

    manager.load_layer(
        "rivers",
        str(RIVERS_FILE),
    )

    assert "rivers" in manager.list_layers()