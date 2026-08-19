import rasterio
import numpy as np
import os

INPUT = "data/ndvi/sentinel2_ndvi.tif"
OUTPUT = "data/ndvi/ndvi_hotspots.tif"

LOW_THRESHOLD = 0.20
HIGH_THRESHOLD = 0.60

print("===== GEOSHIELD NDVI HOTSPOT ENGINE =====")

os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

with rasterio.open(INPUT) as src:
    ndvi = src.read(1)
    profile = src.profile.copy()
    transform = src.transform
    crs = src.crs
    nodata = src.nodata

print("Input:", INPUT)
print("CRS:", crs)
print("Resolution:", transform.a, "m")
print("Shape:", ndvi.shape)

valid = np.isfinite(ndvi)

if nodata is not None:
    valid &= ndvi != nodata

low = valid & (ndvi < LOW_THRESHOLD)
high = valid & (ndvi > HIGH_THRESHOLD)

# 0 = NoData
# 1 = Low vegetation / potential stress
# 2 = Healthy vegetation
# 3 = Very healthy vegetation

hotspots = np.zeros(ndvi.shape, dtype=np.uint8)

hotspots[valid & (ndvi >= LOW_THRESHOLD) & (ndvi <= HIGH_THRESHOLD)] = 2
hotspots[high] = 3
hotspots[low] = 1

profile.update(
    driver="GTiff",
    dtype="uint8",
    count=1,
    nodata=0,
    compress="deflate",
    tiled=True
)

with rasterio.open(OUTPUT, "w", **profile) as dst:
    dst.write(hotspots, 1)

pixel_area_m2 = abs(transform.a * transform.e)

low_pixels = int(low.sum())
healthy_pixels = int(((hotspots == 2)).sum())
high_pixels = int(high.sum())
valid_pixels = int(valid.sum())

print()
print("===== HOTSPOT CLASSIFICATION =====")
print("Low vegetation pixels:", low_pixels)
print("Healthy vegetation pixels:", healthy_pixels)
print("Very healthy pixels:", high_pixels)

print()
print("===== AREA ANALYSIS =====")
print("Pixel area:", pixel_area_m2, "m2")

print(
    "Low vegetation area:",
    round(low_pixels * pixel_area_m2 / 1_000_000, 3),
    "km2"
)

print(
    "Healthy vegetation area:",
    round(healthy_pixels * pixel_area_m2 / 1_000_000, 3),
    "km2"
)

print(
    "Very healthy vegetation area:",
    round(high_pixels * pixel_area_m2 / 1_000_000, 3),
    "km2"
)

if valid_pixels > 0:
    print()
    print("Low vegetation percentage:",
          round(low_pixels / valid_pixels * 100, 3), "%")

    print("Healthy vegetation percentage:",
          round(healthy_pixels / valid_pixels * 100, 3), "%")

    print("Very healthy percentage:",
          round(high_pixels / valid_pixels * 100, 3), "%")

print()
print("Output:", OUTPUT)
print("HOTSPOT ENGINE COMPLETE")
