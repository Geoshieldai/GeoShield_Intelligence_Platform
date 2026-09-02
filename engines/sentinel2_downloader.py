"""
GeoShield AI Enterprise
Sentinel-2 Product Downloader

Uses centralized GeoShield configuration and authentication.
Credentials are never hard-coded.
"""

from __future__ import annotations

import os
from pathlib import Path

import httpx

from core.auth import CopernicusAuthManager
from core.config import settings


DOWNLOAD_URL = (
    "https://download.dataspace.copernicus.eu/"
    "odata/v1/Products"
)

OUTPUT_DIR = Path("data/sentinel2")


class Sentinel2Downloader:
    """Download Sentinel-2 products from Copernicus Data Space."""

    def __init__(
        self,
        auth_manager: CopernicusAuthManager | None = None,
        timeout: float = 600.0,
    ) -> None:

        self.auth_manager = (
            auth_manager
            or CopernicusAuthManager()
        )

        self.timeout = timeout

    def download_product(
        self,
        product_uuid: str,
        output_dir: Path | None = None,
    ) -> Path:
        """
        Download a Copernicus product by UUID.

        Returns:
            Path to downloaded product.
        """

        if not product_uuid.strip():
            raise ValueError(
                "product_uuid cannot be empty."
            )

        destination = (
            output_dir
            or OUTPUT_DIR
        )

        destination.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_file = (
            destination
            / f"{product_uuid}.zip"
        )

        token = self.auth_manager.get_token()

        url = (
            f"{DOWNLOAD_URL}"
            f"({product_uuid})"
            f"/$value"
        )

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/octet-stream",
            "User-Agent": "GeoShield-AI/0.1",
        }

        print(
            "===== GEOSHIELD SENTINEL-2 DOWNLOAD ====="
        )
        print(
            f"Product UUID: {product_uuid}"
        )
        print(
            f"Destination: {output_file}"
        )
        print()
        print(
            "Connecting to Copernicus download service..."
        )

        with httpx.stream(
            "GET",
            url,
            headers=headers,
            timeout=self.timeout,
            follow_redirects=True,
        ) as response:

            print(
                f"DOWNLOAD HTTP: {response.status_code}"
            )

            print(
                "Content-Type:",
                response.headers.get(
                    "content-type"
                ),
            )

            response.raise_for_status()

            total = int(
                response.headers.get(
                    "content-length",
                    "0",
                )
            )

            downloaded = 0

            with open(
                output_file,
                "wb",
            ) as file:

                for chunk in response.iter_bytes(
                    chunk_size=1024 * 1024,
                ):

                    if not chunk:
                        continue

                    file.write(chunk)

                    downloaded += len(chunk)

                    if total:
                        percent = (
                            downloaded
                            / total
                            * 100
                        )

                        print(
                            f"\rDownloaded: "
                            f"{downloaded / 1024 / 1024:.1f} MB "
                            f"({percent:.1f}%)",
                            end="",
                        )

                    else:

                        print(
                            f"\rDownloaded: "
                            f"{downloaded / 1024 / 1024:.1f} MB",
                            end="",
                        )

        print()
        print()
        print(
            "===== DOWNLOAD COMPLETE ====="
        )

        print(
            f"File: {output_file}"
        )

        print(
            f"Size: "
            f"{output_file.stat().st_size:,} bytes"
        )

        return output_file


def main() -> None:
    """
    Manual downloader entry point.

    Replace PRODUCT_UUID with a real UUID returned
    by the Sentinel-2 catalogue search.
    """

    product_uuid = os.getenv(
        "GEOSHIELD_TEST_PRODUCT_UUID",
        "",
    ).strip()

    if not product_uuid:

        raise RuntimeError(
            "GEOSHIELD_TEST_PRODUCT_UUID is not set."
        )

    downloader = Sentinel2Downloader()

    downloader.download_product(
        product_uuid,
    )


if __name__ == "__main__":
    main()