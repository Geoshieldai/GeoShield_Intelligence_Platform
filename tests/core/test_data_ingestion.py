from core.data.ingestion import DataIngestion
from core.data.source import DataSource
from core.data.normalizer import DataNormalizer
from core.data.validator import DataValidator
from core.data.registry import DataSourceRegistry


def test_data_source():
    source = DataSource(
        source_id="S2",
        name="Sentinel-2",
        provider="Copernicus",
        source_type="satellite",
    )

    data = source.to_dict()

    assert data["source_id"] == "S2"
    assert data["provider"] == "Copernicus"


def test_data_ingestion():
    ingestion = DataIngestion()

    dataset = ingestion.ingest(
        dataset_id="TEST001",
        source="Sentinel-2",
        product="L2A",
        data={"B04": "red", "B08": "nir"},
        acquisition_date="2026-08-08",
    )

    assert dataset.dataset_id == "TEST001"
    assert dataset.source == "Sentinel-2"
    assert dataset.product == "L2A"
    assert dataset.metadata["data"]["B04"] == "red"


def test_normalizer():
    normalizer = DataNormalizer()

    observation = normalizer.normalize_observation(
        {
            "latitude": "-1.2921",
            "longitude": "36.8219",
            "source": "VIIRS",
        }
    )

    assert isinstance(observation["latitude"], float)
    assert isinstance(observation["longitude"], float)


def test_normalize_values():
    normalizer = DataNormalizer()

    values = normalizer.normalize_values(
        {
            "brightness": 370,
            "frp": 15,
            "confidence": "high",
        }
    )

    assert values["brightness"] == 370.0
    assert values["frp"] == 15.0
    assert values["confidence"] == "high"


def test_validator():
    validator = DataValidator()

    assert validator.validate_coordinates(
        -1.2921,
        36.8219,
    )

    assert not validator.validate_coordinates(
        100,
        36.8219,
    )


def test_observation_validation():
    validator = DataValidator()

    observation = {
        "observation_id": "OBS001",
        "latitude": -1.2921,
        "longitude": 36.8219,
        "timestamp": "2026-08-08T10:00:00Z",
        "source": "VIIRS",
    }

    assert validator.validate_observation(observation)


def test_invalid_observation():
    validator = DataValidator()

    observation = {
        "observation_id": "OBS002",
        "latitude": 95,
        "longitude": 36.8219,
        "timestamp": "2026-08-08T10:00:00Z",
        "source": "VIIRS",
    }

    assert not validator.validate_observation(observation)


def test_source_registry():
    registry = DataSourceRegistry()

    source = DataSource(
        source_id="VIIRS",
        name="VIIRS Active Fire",
        provider="NASA",
        source_type="satellite",
    )

    registry.register(source)

    assert registry.count() == 1
    assert registry.get("VIIRS") is source
    assert len(registry.list()) == 1