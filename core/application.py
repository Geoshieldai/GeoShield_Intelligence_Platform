"""
GeoShield Intelligence Platform
Enterprise Application Factory

Author:
David Omondi Ouma
Founder & Chief Executive Officer (CEO)
"""

from core.logger import logger
from core.metadata import PROJECT_NAME
from core.version import __version__

from core.service_registry import ServiceRegistry
from core.engine_registry import EngineRegistry

from engines.satellite_engine import SatelliteEngine


class GeoShieldApplication:
    """
    Main GeoShield application bootstrapper.
    Responsible for initializing the platform.
    """

    def __init__(self):

        self.project_name = PROJECT_NAME
        self.version = __version__

        self.initialized = False

        self.services = ServiceRegistry()
        self.engines = EngineRegistry()

    def initialize(self):

        logger.info("Initializing GeoShield Platform...")

        # Register core services
        self.services.register("logger", logger)

        self.services.register(
            "configuration",
            {
                "project": self.project_name,
                "version": self.version,
            },
        )

        logger.info("Loading Engine Registry...")

        satellite_engine = SatelliteEngine()

        satellite_engine.register_provider("Sentinel-1")
        satellite_engine.register_provider("Sentinel-2")
        satellite_engine.register_provider("Landsat")

        self.engines.register(
            "satellite",
            satellite_engine,
        )

        self.initialized = True

        logger.info("Platform initialization completed.")

    def status(self):

        satellite_engine = self.engines.get("satellite")

        if satellite_engine:
            providers = satellite_engine.list_providers()
        else:
            providers = []

        return {
            "project": self.project_name,
            "version": self.version,
            "initialized": self.initialized,
            "registered_services": self.services.list_services(),
            "registered_engines": self.engines.list_engines(),
            "satellite_providers": providers,
        }

    def reload(self):
        """
        Reload the GeoShield platform.
        """

        self.initialize()

        return self.status()