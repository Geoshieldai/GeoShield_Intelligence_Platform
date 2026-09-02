"""
Raster Reader

Reads raster datasets using Rasterio.
"""

import rasterio


class RasterReader:

    def read(self, image_path: str):

        with rasterio.open(image_path) as src:

            return {
                "width": src.width,
                "height": src.height,
                "bands": src.count,
                "crs": str(src.crs),
                "transform": src.transform,
                "bounds": src.bounds,
            }