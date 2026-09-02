import os
import rasterio
import numpy as np
import geopandas as gpd
from rasterio.features import shapes
from shapely.geometry import shape

INPUT = "data/ndvi/ndvi_hotspots.tif"
OUTPUT = "data/ndvi/vegetation_stress_hotspots.geojson"

# Only Class 1 is treated as vegetation stress.
TARGET_CLASS = 1

# Minimum hotspot area.
# 100 pixels × 100 m² = 10,000 m² = 0.01 km²
MIN_PIXELS = 100

WINDOW_SIZE = 1024

print("===== GEOSHIELD MEMORY-SAFE HOTSPOT ENGINE =====")
print("Input:", INPUT)
print("Target class:", TARGET_CLASS)
print("Minimum pixels:", MIN_PIXELS)
print("Window:", WINDOW_SIZE, "x", WINDOW_SIZE)

os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

features = []

with rasterio.open(INPUT) as src:

    print("CRS:", src.crs)
    print("Raster size:", src.width, "x", src.height)
    print("Resolution:", src.res)

    pixel_area_m2 = abs(src.transform.a * src.transform.e)

    windows_total = (
        ((src.height + WINDOW_SIZE - 1) // WINDOW_SIZE)
        *
        ((src.width + WINDOW_SIZE - 1) // WINDOW_SIZE)
    )

    window_number = 0

    for row in range(0, src.height, WINDOW_SIZE):

        for col in range(0, src.width, WINDOW_SIZE):

            window_number += 1

            height = min(WINDOW_SIZE, src.height - row)
            width = min(WINDOW_SIZE, src.width - col)

            window = rasterio.windows.Window(
                col,
                row,
                width,
                height
            )

            raster = src.read(1, window=window)

            mask = raster == TARGET_CLASS

            if not mask.any():
                continue

            window_transform = src.window_transform(window)

            for geom, value in shapes(
                raster,
                mask=mask,
                transform=window_transform
            ):

                if int(value) != TARGET_CLASS:
                    continue

                polygon = shape(geom)

                area_pixels = polygon.area / pixel_area_m2

                if area_pixels < MIN_PIXELS:
                    continue

                features.append({
                    "geometry": polygon,
                    "class": TARGET_CLASS,
                    "area_pixels": int(area_pixels),
                    "area_m2": polygon.area,
                    "area_km2": polygon.area / 1_000_000
                })

            if window_number % 25 == 0:
                print(
                    f"Processed windows: {window_number}/{windows_total} | "
                    f"Hotspots retained: {len(features)}"
                )

    crs = src.crs

print()
print("===== HOTSPOT VECTOR CREATION =====")
print("Candidate polygons retained:", len(features))

if not features:
    print("No hotspots met the minimum-area threshold.")
    raise SystemExit(0)

gdf = gpd.GeoDataFrame(
    features,
    geometry="geometry",
    crs=crs
)

# Add IDs
gdf.insert(
    0,
    "hotspot_id",
    range(1, len(gdf) + 1)
)

gdf["severity"] = "VEGETATION_STRESS"

# Sort largest hotspots first
gdf = gdf.sort_values(
    "area_km2",
    ascending=False
).reset_index(drop=True)

# Reassign IDs after sorting
gdf["hotspot_id"] = range(1, len(gdf) + 1)

gdf.to_file(
    OUTPUT,
    driver="GeoJSON"
)

print()
print("===== HOTSPOT ENGINE COMPLETE =====")
print("Final hotspots:", len(gdf))
print("Output:", OUTPUT)

print()
print("===== AREA SUMMARY =====")
print(
    "Total hotspot area:",
    round(gdf["area_km2"].sum(), 3),
    "km2"
)

print(
    "Largest hotspot:",
    round(gdf["area_km2"].max(), 3),
    "km2"
)

print(
    "Smallest retained hotspot:",
    round(gdf["area_km2"].min(), 6),
    "km2"
)

print()
print("GeoJSON written successfully.")
