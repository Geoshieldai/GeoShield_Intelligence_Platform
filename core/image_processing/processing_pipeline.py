"""
Processing Pipeline

Coordinates image loading, validation,
metadata extraction, and raster reading.
"""

from core.image_processing.image_loader import ImageLoader
from core.image_processing.validator import ImageValidator
from core.image_processing.metadata_reader import MetadataReader
from core.image_processing.raster_reader import RasterReader


class ProcessingPipeline:

    def __init__(self):

        self.loader = ImageLoader()
        self.validator = ImageValidator()
        self.metadata = MetadataReader()
        self.reader = RasterReader()

    def process(self, image_path: str):

        image = self.loader.load(image_path)

        self.validator.validate(image)

        return {
            "metadata": self.metadata.extract(image),
            "raster": self.reader.read(image),
        }