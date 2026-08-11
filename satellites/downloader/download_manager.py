"""
Satellite Download Manager

Routes download requests to the correct provider.
"""

from satellites.sentinel.download import SentinelDownloader
from satellites.landsat.downloader import LandsatDownloader
from satellites.modis.downloader import ModisDownloader
from satellites.viirs.downloader import ViirsDownloader


class DownloadManager:

    def __init__(self):

        self.providers = {
            "Sentinel": SentinelDownloader(),
            "Landsat": LandsatDownloader(),
            "MODIS": ModisDownloader(),
            "VIIRS": ViirsDownloader(),
        }

    def download(
        self,
        provider: str,
        product_id: str,
        destination: str,
    ) -> str:

        downloader = self.providers.get(provider)

        if downloader is None:
            raise ValueError(
                f"No downloader available for {provider}"
            )

        return downloader.download(
            product_id,
            destination,
        )