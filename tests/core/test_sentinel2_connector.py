from core.connectors.sentinel2.sentinel2_config import Sentinel2Config
from core.connectors.sentinel2.sentinel2_product import Sentinel2Product
from core.connectors.sentinel2.sentinel2_search import Sentinel2Search
from core.connectors.sentinel2.sentinel2_connector import Sentinel2Connector


def create_config():
    return Sentinel2Config(
        connector_id="sentinel2",
        provider="Copernicus",
        base_url="https://example.com",
    )


def test_sentinel2_config():
    config = create_config()

    assert config.validate()
    assert config.collection == "SENTINEL-2"
    assert config.processing_level == "L2A"


def test_invalid_cloud_cover():
    config = Sentinel2Config(
        connector_id="sentinel2",
        provider="Copernicus",
        cloud_cover_max=120,
    )

    assert not config.validate()


def test_sentinel2_product():
    product = Sentinel2Product(
        product_id="S2_TEST_001",
        acquisition_date="2026-08-08",
        cloud_cover=12.5,
        tile_id="T37MBV",
    )

    data = product.to_dict()

    assert data["product_id"] == "S2_TEST_001"
    assert data["processing_level"] == "L2A"
    assert data["cloud_cover"] == 12.5
    assert data["tile_id"] == "T37MBV"


def test_sentinel2_search_model():
    search = Sentinel2Search(
        start_date="2026-08-01",
        end_date="2026-08-08",
        latitude=-1.2921,
        longitude=36.8219,
        cloud_cover_max=20,
        tile_id="T37MBV",
    )

    assert search.validate()

    data = search.to_dict()

    assert data["latitude"] == -1.2921
    assert data["longitude"] == 36.8219
    assert data["cloud_cover_max"] == 20


def test_invalid_search_coordinates():
    search = Sentinel2Search(
        latitude=100,
        longitude=36.8219,
    )

    assert not search.validate()


def test_sentinel2_connector():
    connector = Sentinel2Connector(create_config())

    assert connector.provider_name == "Sentinel-2"
    assert connector.is_enabled()


def test_sentinel2_connect():
    connector = Sentinel2Connector(create_config())

    result = connector.connect()

    assert result.success
    assert result.provider == "Sentinel-2"
    assert result.operation == "connect"
    assert result.data["status"] == "ready"


def test_sentinel2_connector_search():
    connector = Sentinel2Connector(create_config())

    result = connector.search(
        start_date="2026-08-01",
        end_date="2026-08-08",
        latitude=-1.2921,
        longitude=36.8219,
        cloud_cover_max=20,
    )

    assert result.success
    assert result.operation == "search"
    assert result.data["status"] == "search_ready"


def test_sentinel2_download():
    connector = Sentinel2Connector(create_config())

    result = connector.download("S2_TEST_001")

    assert result.success
    assert result.operation == "download"
    assert result.data["product_id"] == "S2_TEST_001"


def test_invalid_download():
    connector = Sentinel2Connector(create_config())

    result = connector.download("")

    assert not result.success
    assert result.error == "Product ID is required"


def test_create_sentinel2_product():
    connector = Sentinel2Connector(create_config())

    product = connector.create_product(
        product_id="S2_TEST_002",
        acquisition_date="2026-08-08",
        cloud_cover=5.5,
        tile_id="T37MBV",
        product_name="Sentinel Test Product",
    )

    assert product.product_id == "S2_TEST_002"
    assert product.processing_level == "L2A"
    assert product.cloud_cover == 5.5
    assert product.tile_id == "T37MBV"