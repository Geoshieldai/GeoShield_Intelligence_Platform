"""
GeoShield Intelligence Platform

Sentinel Provider

Author:
David Omondi Ouma
Founder & Chief Executive Officer (CEO)
"""

from satellites.base.provider import SatelliteProvider
from satellites.base.authentication import AuthenticationManager
from satellites.base.downloader import Downloader
from satellites.base.metadata import MetadataManager


class SentinelProvider(SatelliteProvider):

    def __init__(self):

        super().__init__("Copernicus Sentinel")

        self.authentication = AuthenticationManager()
        self.downloader = Downloader()
        self.metadata_manager = MetadataManager()

    def authenticate(self):

        self.authentication.login()

        return self.authentication.status()

    def search(self, **kwargs):

        return [
            {
                "product_id": "S2A_TEST_001",
                "date": "2026-08-03",
                "cloud_cover": 4,
            },
            {
                "product_id": "S2B_TEST_002",
                "date": "2026-08-01",
                "cloud_cover": 11,
            },
        ]

    def download(self, product_id):

        url = f"https://dataspace.copernicus.eu/{product_id}"

        return self.downloader.download(url)

    def metadata(self, product_id):

        metadata = self.metadata_manager.create()

        metadata["provider"] = self.provider_name
        metadata["product_id"] = product_id
        metadata["date"] = "2026-08-03"
        metadata["cloud_cover"] = 4
        metadata["resolution"] = "10 m"

        return metadata