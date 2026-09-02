import geopandas as gpd
import numpy as np
import os

INPUT = "data/ndvi/vegetation_stress_impact.geojson"
OUTPUT = "data/ndvi/vegetation_risk_intelligence.geojson"

print("===== GEOSHIELD RISK INTELLIGENCE ENGINE =====")

gdf = gpd.read_file(INPUT)

print("Input:", INPUT)
print("Hotspots loaded:", len(gdf))
print("CRS:", gdf.crs)

# ---------------------------------------------------------
# NORMALIZE IMPACT SCORE
# ---------------------------------------------------------

impact_min = gdf["impact_score"].min()
impact_max = gdf["impact_score"].max()

if impact_max > impact_min:
    gdf["impact_normalized"] = (
        (gdf["impact_score"] - impact_min)
        / (impact_max - impact_min)
    )
else:
    gdf["impact_normalized"] = 0.0

# ---------------------------------------------------------
# NDVI STRESS COMPONENT
# Lower NDVI = greater vegetation stress
# ---------------------------------------------------------

gdf["ndvi_stress"] = np.clip(
    (0.20 - gdf["mean_ndvi"]) / 1.20,
    0,
    1
)

# ---------------------------------------------------------
# AREA COMPONENT
# Larger affected areas receive greater risk weight
# ---------------------------------------------------------

area_max = gdf["geometry_area_km2"].max()

if area_max > 0:
    gdf["area_normalized"] = (
        gdf["geometry_area_km2"] / area_max
    )
else:
    gdf["area_normalized"] = 0.0

# ---------------------------------------------------------
# RISK SCORE
# ---------------------------------------------------------

gdf["risk_score"] = (
    gdf["impact_normalized"] * 0.50
    + gdf["ndvi_stress"] * 0.35
    + gdf["area_normalized"] * 0.15
) * 100

# ---------------------------------------------------------
# RISK CLASSIFICATION
# ---------------------------------------------------------

def classify_risk(score):
    if score >= 80:
        return "EXTREME"
    elif score >= 60:
        return "HIGH"
    elif score >= 40:
        return "MODERATE"
    elif score >= 20:
        return "LOW"
    else:
        return "MINIMAL"

gdf["risk_class"] = gdf["risk_score"].apply(classify_risk)

# ---------------------------------------------------------
# OPERATIONAL ACTION
# ---------------------------------------------------------

def action_for_risk(risk):
    if risk == "EXTREME":
        return "IMMEDIATE_FIELD_ASSESSMENT"
    elif risk == "HIGH":
        return "PRIORITY_MONITORING"
    elif risk == "MODERATE":
        return "ENHANCED_MONITORING"
    elif risk == "LOW":
        return "ROUTINE_MONITORING"
    else:
        return "NO_IMMEDIATE_ACTION"

gdf["recommended_action"] = gdf["risk_class"].apply(
    action_for_risk
)

# ---------------------------------------------------------
# RANK
# ---------------------------------------------------------

gdf = gdf.sort_values(
    "risk_score",
    ascending=False
).reset_index(drop=True)

gdf["risk_rank"] = np.arange(1, len(gdf) + 1)

# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------

print()
print("===== RISK SUMMARY =====")

print("Total hotspots:", len(gdf))
print(
    "Mean risk score:",
    round(float(gdf["risk_score"].mean()), 3)
)

print(
    "Maximum risk score:",
    round(float(gdf["risk_score"].max()), 3)
)

print()
print("===== RISK DISTRIBUTION =====")
print(gdf["risk_class"].value_counts())

print()
print("===== TOP 10 RISK AREAS =====")

cols = [
    "risk_rank",
    "geometry_area_km2",
    "mean_ndvi",
    "impact_score",
    "risk_score",
    "risk_class",
    "recommended_action"
]

print(
    gdf[cols]
    .head(10)
    .to_string(index=False)
)

# ---------------------------------------------------------
# OUTPUT
# ---------------------------------------------------------

os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

gdf.to_file(
    OUTPUT,
    driver="GeoJSON"
)

print()
print("Output:", OUTPUT)
print("RISK INTELLIGENCE ENGINE COMPLETE")
