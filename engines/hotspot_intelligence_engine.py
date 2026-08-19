import geopandas as gpd
import rasterio
import numpy as np
from rasterio.mask import mask
import os

HOTSPOTS = "data/ndvi/vegetation_stress_hotspots.geojson"
NDVI = "data/ndvi/sentinel2_ndvi.tif"
OUTPUT = "data/ndvi/vegetation_stress_intelligence.geojson"

print("===== GEOSHIELD TRUE NDVI INTELLIGENCE ENGINE =====")

gdf = gpd.read_file(HOTSPOTS)

print("Hotspots:", len(gdf))
print("Hotspot CRS:", gdf.crs)

with rasterio.open(NDVI) as src:

    print("NDVI CRS:", src.crs)
    print("NDVI resolution:", src.res)

    # Match hotspot CRS to raster CRS
    gdf = gdf.to_crs(src.crs)

    mean_values = []
    min_values = []
    max_values = []
    valid_pixels = []

    total = len(gdf)

    print()
    print("Extracting NDVI statistics...")

    for i, geometry in enumerate(gdf.geometry):

        try:
            data, _ = mask(
                src,
                [geometry],
                crop=True,
                nodata=-9999
            )

            values = data[0].astype("float32")

            values = values[
                np.isfinite(values) &
                (values != -9999)
            ]

            if values.size == 0:
                mean_values.append(np.nan)
                min_values.append(np.nan)
                max_values.append(np.nan)
                valid_pixels.append(0)
            else:
                mean_values.append(float(np.mean(values)))
                min_values.append(float(np.min(values)))
                max_values.append(float(np.max(values)))
                valid_pixels.append(int(values.size))

        except Exception:
            mean_values.append(np.nan)
            min_values.append(np.nan)
            max_values.append(np.nan)
            valid_pixels.append(0)

        if (i + 1) % 250 == 0 or i + 1 == total:
            print(
                f"Processed: {i + 1}/{total}"
            )

gdf["mean_ndvi"] = mean_values
gdf["min_ndvi"] = min_values
gdf["max_ndvi"] = max_values
gdf["valid_pixels"] = valid_pixels

# Accurate area
metric = gdf.to_crs("EPSG:32737")

metric["area_km2"] = (
    metric.geometry.area / 1_000_000
)

# --------------------------------------------------
# TRUE NDVI SEVERITY
# --------------------------------------------------

metric["severity"] = np.select(
    [
        metric["mean_ndvi"] < 0.10,
        metric["mean_ndvi"] < 0.20,
        metric["mean_ndvi"] < 0.30,
        metric["mean_ndvi"] < 0.45,
        metric["mean_ndvi"] >= 0.45
    ],
    [
        "CRITICAL",
        "SEVERE",
        "HIGH",
        "MODERATE",
        "LOW"
    ],
    default="UNKNOWN"
)

severity_weight = {
    "CRITICAL": 5,
    "SEVERE": 4,
    "HIGH": 3,
    "MODERATE": 2,
    "LOW": 1,
    "UNKNOWN": 0
}

metric["severity_weight"] = (
    metric["severity"]
    .map(severity_weight)
    .fillna(0)
)

# --------------------------------------------------
# PRIORITY SCORE
# --------------------------------------------------

metric["priority_score"] = (
    metric["severity_weight"]
    * np.log1p(metric["area_km2"])
)

metric["priority"] = np.select(
    [
        metric["priority_score"] >= 20,
        metric["priority_score"] >= 12,
        metric["priority_score"] >= 6,
        metric["priority_score"] >= 2
    ],
    [
        "URGENT",
        "HIGH",
        "MEDIUM",
        "LOW"
    ],
    default="LOW"
)

# Rank
metric = metric.sort_values(
    "priority_score",
    ascending=False
).reset_index(drop=True)

metric["hotspot_rank"] = (
    np.arange(1, len(metric) + 1)
)

# Return to original geographic CRS
output = metric.to_crs(gdf.crs)

os.makedirs(
    os.path.dirname(OUTPUT),
    exist_ok=True
)

output.to_file(
    OUTPUT,
    driver="GeoJSON"
)

# --------------------------------------------------
# REPORT
# --------------------------------------------------

print()
print("===== TRUE NDVI INTELLIGENCE SUMMARY =====")

print("Total hotspots:", len(output))

print(
    "Total hotspot area:",
    round(float(output["area_km2"].sum()), 3),
    "km2"
)

print(
    "Largest hotspot:",
    round(float(output["area_km2"].max()), 3),
    "km2"
)

print()
print("NDVI statistics:")

print(
    "Mean NDVI:",
    round(float(output["mean_ndvi"].mean()), 4)
)

print(
    "Minimum NDVI:",
    round(float(output["min_ndvi"].min()), 4)
)

print(
    "Maximum NDVI:",
    round(float(output["max_ndvi"].max()), 4)
)

print()
print("===== SEVERITY DISTRIBUTION =====")

print(
    output["severity"]
    .value_counts()
    .to_string()
)

print()
print("===== PRIORITY DISTRIBUTION =====")

print(
    output["priority"]
    .value_counts()
    .to_string()
)

print()
print("===== TOP 10 HOTSPOTS =====")

columns = [
    "hotspot_rank",
    "area_km2",
    "mean_ndvi",
    "min_ndvi",
    "max_ndvi",
    "severity",
    "priority",
    "priority_score"
]

print(
    output[columns]
    .head(10)
    .to_string(index=False)
)

print()
print("Output:", OUTPUT)
print("TRUE NDVI INTELLIGENCE ENGINE COMPLETE")
