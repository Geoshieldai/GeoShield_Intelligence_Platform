"""
Landsat Downloader
"""

from satellites.downloader.base_downloader import BaseDownloader


class LandsatDownloader(BaseDownloader):

    def download(
        self,
        product_id: str,
        destination: str,
    ):

        print(
            f"Downloading Landsat product {product_id}"
        )

        return f"{destination}/{product_id}.zip"