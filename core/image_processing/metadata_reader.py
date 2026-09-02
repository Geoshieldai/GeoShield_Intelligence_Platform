"""
Metadata Reader

Extracts metadata from raster datasets.
"""

import rasterio


class MetadataReader:

    def extract(self, image_path: str):

        with rasterio.open(image_path) as src:

            return src.meta