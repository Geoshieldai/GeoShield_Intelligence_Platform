"""
Band Extractor

Extracts image bands from raster datasets.
"""

import rasterio


class BandExtractor:

    def extract(self, image_path: str, band_number: int):

        with rasterio.open(image_path) as src:

            if band_number > src.count:
                raise ValueError(
                    f"Band {band_number} not found."
                )

            return src.read(band_number)