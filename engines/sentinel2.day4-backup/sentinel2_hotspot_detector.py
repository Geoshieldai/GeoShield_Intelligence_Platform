import os
import numpy as np
import rasterio
from rasterio.features import shapes
from shapely.geometry import shape
import geopandas as gpd

# ============================================================
# GEOSHIELD SENTINEL-2 HOTSPOT DETECTOR
# ============================================================

NDVI_PATH = (
    "data/ndvi/"
    "sentinel2_20260812_T37MBU_ndvi.tif"
)

OUTPUT_DIR = "data/ndvi"

OUTPUT_PATH = (
    OUTPUT_DIR
    + "/sentinel2_20260812_T37MBU_hotspots.geojson"
)

# NDVI below this threshold is treated as vegetation stress.
STRESS_THRESHOLD = 0.20

# Ignore tiny fragments.
MIN_AREA_KM2 = 0.01

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("===== GEOSHIELD SENTINEL-2 HOTSPOT DETECTOR =====")

if not os.path.exists(NDVI_PATH):
    raise FileNotFoundError(
        f"NDVI raster not found: {NDVI_PATH}"
    )

with rasterio.open(NDVI_PATH) as src:
    ndvi = src.read(1)
    transform = src.transform
    crs = src.crs

print("Input:", NDVI_PATH)
print("CRS:", crs)
print("Stress threshold:", STRESS_THRESHOLD)

valid = np.isfinite(ndvi)

stress_mask = (
    valid
    & (ndvi < STRESS_THRESHOLD)
)

print()
print("Valid NDVI pixels:", int(valid.sum()))
print("Stress pixels:", int(stress_mask.sum()))

# ------------------------------------------------------------
# Polygonize the stress mask
# ------------------------------------------------------------

records = []

for geometry, value in shapes(
    stress_mask.astype(np.uint8),
    mask=stress_mask,
    transform=transform,
):
    if value != 1:
        continue

    polygon = shape(geometry)

    if polygon.is_empty:
        continue

    area_km2 = polygon.area / 1_000_000.0

    if area_km2 < MIN_AREA_KM2:
        continue

    records.append(
        {
            "geometry": polygon,
            "area_km2": area_km2,
            "stress_threshold": STRESS_THRESHOLD,
        }
    )

print()
print("Raw stress polygons:", len(records))

if not records:
    print()
    print("No vegetation-stress hotspots detected.")
    print("Try adjusting STRESS_THRESHOLD.")
    raise SystemExit(0)

gdf = gpd.GeoDataFrame(
    records,
    crs=crs,
)

# ------------------------------------------------------------
# Calculate mean NDVI inside each hotspot
# ------------------------------------------------------------

mean_values = []

with rasterio.open(NDVI_PATH) as src:

    from rasterio.mask import mask

    for geometry in gdf.geometry:

        try:
            clipped, _ = mask(
                src,
                [geometry],
                crop=True,
                nodata=np.nan,
            )

            values = clipped[0]

            values = values[
                np.isfinite(values)
            ]

            if len(values):
                mean_values.append(
                    float(np.mean(values))
                )
            else:
                mean_values.append(np.nan)

        except Exception:
            mean_values.append(np.nan)

gdf["mean_ndvi"] = mean_values

# ------------------------------------------------------------
# Severity classification
# ------------------------------------------------------------

def classify_severity(ndvi_value):

    if not np.isfinite(ndvi_value):
        return "UNKNOWN"

    if ndvi_value < 0.05:
        return "CRITICAL"

    if ndvi_value < 0.15:
        return "SEVERE"

    if ndvi_value < 0.20:
        return "MODERATE"

    return "LOW"


gdf["severity"] = gdf["mean_ndvi"].apply(
    classify_severity
)

# Rank largest/stressed areas first.

gdf = gdf.sort_values(
    ["severity", "area_km2"],
    ascending=[True, False],
).reset_index(drop=True)

gdf["hotspot_rank"] = (
    np.arange(len(gdf)) + 1
)

gdf["hotspot_id"] = [
    f"S2-{i:06d}"
    for i in range(1, len(gdf) + 1)
]

gdf.to_file(
    OUTPUT_PATH,
    driver="GeoJSON",
)

print()
print("===== HOTSPOT SUMMARY =====")
print("Hotspots:", len(gdf))
print(
    "Total area km2:",
    round(float(gdf.area_km2.sum()), 3)
)
print(
    "Largest hotspot km2:",
    round(float(gdf.area_km2.max()), 3)
)

print()
print("===== SEVERITY DISTRIBUTION =====")
print(
    gdf["severity"].value_counts()
)

print()
print("Output:", OUTPUT_PATH)
print()
print("SENTINEL-2 HOTSPOT DETECTOR COMPLETE")
