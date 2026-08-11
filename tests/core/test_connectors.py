from core.connectors.base_connector import BaseConnector
from core.connectors.connector_config import ConnectorConfig
from core.connectors.connector_registry import ConnectorRegistry
from core.connectors.connector_result import ConnectorResult


class MockConnector(BaseConnector):
    """Test connector used to verify the connector interface."""

    @property
    def provider_name(self) -> str:
        return "MockProvider"

    def connect(self) -> ConnectorResult:
        return ConnectorResult.ok(
            provider=self.provider_name,
            operation="connect",
        )

    def search(self, **filters) -> ConnectorResult:
        return ConnectorResult.ok(
            provider=self.provider_name,
            operation="search",
            data=filters,
        )

    def download(self, product_id: str) -> ConnectorResult:
        return ConnectorResult.ok(
            provider=self.provider_name,
            operation="download",
            data={"product_id": product_id},
        )


def test_connector_config():
    config = ConnectorConfig(
        connector_id="sentinel2",
        provider="Sentinel-2",
        base_url="https://example.com",
    )

    assert config.validate()
    assert config.enabled
    assert config.timeout == 30.0
    assert config.retries == 3


def test_invalid_connector_config():
    config = ConnectorConfig(
        connector_id="",
        provider="Sentinel-2",
    )

    assert not config.validate()


def test_connector_result_success():
    result = ConnectorResult.ok(
        provider="Sentinel-2",
        operation="connect",
        data={"status": "connected"},
    )

    assert result.success
    assert result.provider == "Sentinel-2"
    assert result.operation == "connect"
    assert result.data["status"] == "connected"
    assert result.error is None


def test_connector_result_failure():
    result = ConnectorResult.failure(
        provider="Sentinel-2",
        operation="connect",
        error="Connection failed",
    )

    assert not result.success
    assert result.error == "Connection failed"


def test_mock_connector():
    config = ConnectorConfig(
        connector_id="mock",
        provider="MockProvider",
    )

    connector = MockConnector(config)

    assert connector.provider_name == "MockProvider"
    assert connector.is_enabled()

    result = connector.connect()

    assert result.success
    assert result.operation == "connect"


def test_connector_search():
    config = ConnectorConfig(
        connector_id="mock",
        provider="MockProvider",
    )

    connector = MockConnector(config)

    result = connector.search(
        latitude=-1.2921,
        longitude=36.8219,
    )

    assert result.success
    assert result.data["latitude"] == -1.2921
    assert result.data["longitude"] == 36.8219


def test_connector_download():
    config = ConnectorConfig(
        connector_id="mock",
        provider="MockProvider",
    )

    connector = MockConnector(config)

    result = connector.download("TEST_PRODUCT")

    assert result.success
    assert result.data["product_id"] == "TEST_PRODUCT"


def test_connector_registry():
    registry = ConnectorRegistry()

    config = ConnectorConfig(
        connector_id="mock",
        provider="MockProvider",
    )

    connector = MockConnector(config)

    registry.register(connector)

    assert registry.count() == 1
    assert registry.get("MockProvider") is connector
    assert len(registry.list()) == 1


def test_connector_registry_remove():
    registry = ConnectorRegistry()

    config = ConnectorConfig(
        connector_id="mock",
        provider="MockProvider",
    )

    connector = MockConnector(config)

    registry.register(connector)

    assert registry.remove("MockProvider")
    assert registry.count() == 0
    assert registry.get("MockProvider") is None


def test_connector_registry_clear():
    registry = ConnectorRegistry()

    config = ConnectorConfig(
        connector_id="mock",
        provider="MockProvider",
    )

    connector = MockConnector(config)

    registry.register(connector)

    registry.clear()

    assert registry.count() == 0