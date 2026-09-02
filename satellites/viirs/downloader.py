"""
VIIRS Downloader
"""

from satellites.downloader.base_downloader import BaseDownloader


class ViirsDownloader(BaseDownloader):

    def download(
        self,
        product_id: str,
        destination: str,
    ):

        print(
            f"Downloading VIIRS product {product_id}"
        )

        return f"{destination}/{product_id}.zip"