"""
MODIS Downloader
"""

from satellites.downloader.base_downloader import BaseDownloader


class ModisDownloader(BaseDownloader):

    def download(
        self,
        product_id: str,
        destination: str,
    ):

        print(
            f"Downloading MODIS product {product_id}"
        )

        return f"{destination}/{product_id}.zip"