"""
GeoShield Sentinel-2 Downloader

Prepares Sentinel-2 product download operations.

Actual network downloading will be enabled during the live
provider integration stage.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Sentinel2DownloadRequest:
    """
    Standard Sentinel-2 download request.
    """

    product_id: str
    destination: str

    def validate(self) -> bool:
        """
        Validate the download request.
        """

        return bool(
            self.product_id.strip()
            and self.destination.strip()
        )

    def to_dict(self) -> dict[str, str]:
        """
        Convert the request to a dictionary.
        """

        return {
            "product_id": self.product_id,
            "destination": self.destination,
        }


class Sentinel2Downloader:
    """
    Prepare Sentinel-2 product downloads.
    """

    def create_request(
        self,
        product_id: str,
        destination: str,
    ) -> Sentinel2DownloadRequest:
        """
        Create and validate a download request.
        """

        request = Sentinel2DownloadRequest(
            product_id=product_id,
            destination=destination,
        )

        if not request.validate():
            raise ValueError(
                "Valid product ID and destination are required."
            )

        return request

    def prepare(
        self,
        request: Sentinel2DownloadRequest,
    ) -> dict[str, object]:
        """
        Prepare a download operation without performing it.
        """

        if not request.validate():
            raise ValueError("Invalid Sentinel-2 download request.")

        return {
            "status": "download_ready",
            "product_id": request.product_id,
            "destination": request.destination,
        }