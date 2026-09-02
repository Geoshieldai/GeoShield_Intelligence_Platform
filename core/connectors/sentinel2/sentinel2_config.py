"""
GeoShield Sentinel-2 Configuration
"""

from dataclasses import dataclass

from core.connectors.connector_config import ConnectorConfig


@dataclass
class Sentinel2Config(ConnectorConfig):
    """Configuration specific to Sentinel-2."""

    connector_id: str = "sentinel2"
    provider: str = "Sentinel-2"
    collection: str = "SENTINEL-2"
    processing_level: str = "L2A"
    cloud_cover_max: float = 100.0

    def validate(self) -> bool:
        """Validate Sentinel-2 configuration."""

        if not super().validate():
            return False

        if not 0 <= self.cloud_cover_max <= 100:
            return False

        if not self.collection:
            return False

        if not self.processing_level:
            return False

        return True