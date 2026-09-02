from core.data.dataset import GeoDataset
from core.data.raster_dataset import RasterDataset
from core.data.observation import Observation
from core.data.catalog import DatasetCatalog


def test_geo_dataset():
    dataset = GeoDataset(
        dataset_id="TEST001",
        source="Sentinel-2",
        product="L2A",
        acquisition_date="2026-08-01",
    )

    data = dataset.to_dict()

    assert data["dataset_id"] == "TEST001"
    assert data["source"] == "Sentinel-2"


def test_raster_dataset():
    dataset = RasterDataset(
        dataset_id="RASTER001",
        source="Sentinel-2",
        product="B04",
        file_path="data/test.tif",
        bands=["B04"],
        width=100,
        height=100,
        crs="EPSG:4326",
    )

    data = dataset.to_dict()

    assert data["file_path"] == "data/test.tif"
    assert data["bands"] == ["B04"]
    assert data["width"] == 100


def test_observation():
    observation = Observation(
        observation_id="OBS001",
        latitude=-1.2921,
        longitude=36.8219,
        timestamp="2026-08-01T10:00:00Z",
        source="VIIRS",
        values={
            "brightness": 370,
            "frp": 15,
        },
    )

    data = observation.to_dict()

    assert data["latitude"] == -1.2921
    assert data["longitude"] == 36.8219
    assert data["source"] == "VIIRS"
    assert data["values"]["frp"] == 15


def test_dataset_catalog():
    catalog = DatasetCatalog()

    dataset = GeoDataset(
        dataset_id="CAT001",
        source="Sentinel-2",
        product="L2A",
    )

    catalog.register(dataset)

    assert catalog.count() == 1
    assert catalog.get("CAT001") is dataset
    assert len(catalog.list()) == 1