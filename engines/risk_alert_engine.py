import geopandas as gpd
import os
from datetime import datetime, timezone

INPUT = "data/ndvi/vegetation_risk_intelligence.geojson"
OUTPUT = "data/ndvi/geoshield_risk_alerts.geojson"

print("===== GEOSHIELD RISK ALERT ENGINE =====")

gdf = gpd.read_file(INPUT)

print("Input:", INPUT)
print("Risk areas loaded:", len(gdf))
print("CRS:", gdf.crs)

# ---------------------------------------------------------
# ALERT CLASSIFICATION
# ---------------------------------------------------------

def alert_level(row):

    risk = float(row["risk_score"])

    if risk >= 60:
        return "CRITICAL"

    elif risk >= 40:
        return "HIGH"

    elif risk >= 20:
        return "WATCH"

    else:
        return "INFORMATIONAL"


def alert_action(level):

    if level == "CRITICAL":
        return "IMMEDIATE_RESPONSE"

    elif level == "HIGH":
        return "FIELD_ASSESSMENT"

    elif level == "WATCH":
        return "ENHANCED_MONITORING"

    else:
        return "ROUTINE_MONITORING"


def alert_message(level):

    if level == "CRITICAL":
        return "Severe vegetation stress detected. Immediate assessment recommended."

    elif level == "HIGH":
        return "Significant vegetation stress detected. Field assessment recommended."

    elif level == "WATCH":
        return "Vegetation stress detected. Enhanced monitoring recommended."

    else:
        return "Vegetation condition within low-risk range."


# ---------------------------------------------------------
# GENERATE ALERT ATTRIBUTES
# ---------------------------------------------------------

gdf["alert_level"] = gdf.apply(
    alert_level,
    axis=1
)

gdf["alert_action"] = gdf["alert_level"].apply(
    alert_action
)

gdf["alert_message"] = gdf["alert_level"].apply(
    alert_message
)

gdf["alert_id"] = [
    f"GS-{i:06d}"
    for i in range(1, len(gdf) + 1)
]

gdf["alert_timestamp"] = datetime.now(
    timezone.utc
).isoformat()

# ---------------------------------------------------------
# PRIORITY ORDER
# ---------------------------------------------------------

priority_order = {
    "CRITICAL": 1,
    "HIGH": 2,
    "WATCH": 3,
    "INFORMATIONAL": 4
}

gdf["alert_priority"] = gdf["alert_level"].map(
    priority_order
)

gdf = gdf.sort_values(
    ["alert_priority", "risk_score"],
    ascending=[True, False]
).reset_index(drop=True)

gdf["alert_rank"] = range(
    1,
    len(gdf) + 1
)

# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------

print()
print("===== ALERT SUMMARY =====")

print(
    "Total alerts:",
    len(gdf)
)

print()
print("===== ALERT DISTRIBUTION =====")

print(
    gdf["alert_level"].value_counts()
)

# ---------------------------------------------------------
# TOP ALERTS
# ---------------------------------------------------------

print()
print("===== TOP 10 ALERTS =====")

columns = [
    "alert_rank",
    "alert_id",
    "geometry_area_km2",
    "mean_ndvi",
    "risk_score",
    "risk_class",
    "alert_level",
    "alert_action"
]

print(
    gdf[columns]
    .head(10)
    .to_string(index=False)
)

# ---------------------------------------------------------
# OUTPUT
# ---------------------------------------------------------

os.makedirs(
    os.path.dirname(OUTPUT),
    exist_ok=True
)

gdf.to_file(
    OUTPUT,
    driver="GeoJSON"
)

print()
print("Output:", OUTPUT)
print("RISK ALERT ENGINE COMPLETE")
