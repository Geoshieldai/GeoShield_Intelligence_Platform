"""
Sentinel Downloader
"""

from satellites.downloader.base_downloader import BaseDownloader


class SentinelDownloader(BaseDownloader):

    def download(
        self,
        product_id: str,
        destination: str,
    ):

        print(
            f"Downloading Sentinel product {product_id}"
        )

        return f"{destination}/{product_id}.zip"