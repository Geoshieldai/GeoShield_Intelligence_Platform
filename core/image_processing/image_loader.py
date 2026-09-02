"""
Image Loader

Loads raster datasets from disk.
"""

from pathlib import Path


class ImageLoader:

    def load(self, image_path: str):

        path = Path(image_path)

        if not path.exists():
            raise FileNotFoundError(path)

        return str(path)