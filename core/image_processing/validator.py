"""
Image Validator

Checks whether a raster image is suitable for processing.
"""

import rasterio


class ImageValidator:

    def validate(self, image_path: str):

        with rasterio.open(image_path) as src:

            if src.count == 0:
                raise ValueError("Image contains no bands.")

            if src.width <= 0 or src.height <= 0:
                raise ValueError("Invalid raster dimensions.")

            return True