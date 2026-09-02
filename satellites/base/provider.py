"""
GeoShield Intelligence Platform

Base Satellite Provider

Author:
David Omondi Ouma
Founder & Chief Executive Officer (CEO)
"""


from abc import ABC, abstractmethod


class SatelliteProvider(ABC):
    """
    Abstract base class for all satellite providers.
    """

    def __init__(self, provider_name: str):

        self.provider_name = provider_name

    @abstractmethod
    def authenticate(self):
        """
        Authenticate with the provider.
        """
        pass

    @abstractmethod
    def search(self, **kwargs):
        """
        Search available imagery.
        """
        pass

    @abstractmethod
    def download(self, product_id):
        """
        Download imagery.
        """
        pass

    @abstractmethod
    def metadata(self, product_id):
        """
        Retrieve imagery metadata.
        """
        pass

    def info(self):

        return {
            "provider": self.provider_name
        }