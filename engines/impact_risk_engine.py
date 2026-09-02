import geopandas as gpd
import pandas as pd
import os

INPUT = "data/ndvi/vegetation_stress_intelligence.geojson"
OUTPUT = "data/ndvi/vegetation_stress_impact.geojson"

print("===== GEOSHIELD IMPACT FOUNDATION ENGINE =====")
print("Input:", INPUT)

gdf = gpd.read_file(INPUT)

print("Hotspots loaded:", len(gdf))
print("CRS:", gdf.crs)

# Ensure projected CRS for accurate area calculations
if gdf.crs is None:
    raise ValueError("Input GeoJSON has no CRS.")

if not gdf.crs.is_projected:
    gdf = gdf.to_crs("EPSG:32737")

# Recalculate geometry area
gdf["geometry_area_km2"] = gdf.geometry.area / 1_000_000

# Basic geographic descriptors
gdf["centroid_x"] = gdf.geometry.centroid.x
gdf["centroid_y"] = gdf.geometry.centroid.y

# Keep the existing intelligence fields
if "priority_score" in gdf.columns:
    gdf["impact_score"] = (
        gdf["priority_score"]
        * (1 + gdf["geometry_area_km2"] / gdf["geometry_area_km2"].max())
    )
else:
    gdf["impact_score"] = (
        gdf["geometry_area_km2"]
        / gdf["geometry_area_km2"].max()
    )

gdf["impact_rank"] = (
    gdf["impact_score"]
    .rank(method="dense", ascending=False)
    .astype(int)
)

# Sort highest-impact areas first
gdf = gdf.sort_values("impact_score", ascending=False)

os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

gdf.to_file(
    OUTPUT,
    driver="GeoJSON"
)

print()
print("===== IMPACT SUMMARY =====")
print("Total hotspots:", len(gdf))
print(
    "Total area km2:",
    round(float(gdf["geometry_area_km2"].sum()), 3)
)
print(
    "Largest hotspot km2:",
    round(float(gdf["geometry_area_km2"].max()), 3)
)
print(
    "Mean hotspot area km2:",
    round(float(gdf["geometry_area_km2"].mean()), 4)
)

print()
print("===== TOP 10 IMPACT AREAS =====")
cols = [
    "impact_rank",
    "geometry_area_km2",
    "mean_ndvi",
    "severity",
    "priority",
    "impact_score"
]

available = [c for c in cols if c in gdf.columns]

print(
    gdf[available]
    .head(10)
    .to_string(index=False)
)

print()
print("Output:", OUTPUT)
print("IMPACT FOUNDATION ENGINE COMPLETE")
