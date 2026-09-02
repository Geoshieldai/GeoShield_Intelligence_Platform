import httpx

print("===== GeoShield Sentinel-2 STAC Search =====")

STAC_URL = "https://stac.dataspace.copernicus.eu/v1/search"

# Nairobi approximate bounding box
# west, south, east, north
bbox = [
    36.65,
    -1.45,
    37.10,
    -1.15,
]

params = {
    "collections": "sentinel-2-l2a",
    "bbox": ",".join(str(x) for x in bbox),
    "datetime": "2026-08-01T00:00:00Z/2026-08-13T23:59:59Z",
    "limit": 5,
}

print("STAC endpoint:", STAC_URL)
print("Area: Nairobi region")
print("Collection: Sentinel-2 L2A")
print("Maximum results: 5")
print("")

try:
    response = httpx.get(
        STAC_URL,
        params=params,
        timeout=60,
    )

    print("HTTP status:", response.status_code)

    response.raise_for_status()

    data = response.json()
    features = data.get("features", [])

    print("STAC search: SUCCESS")
    print("Products found:", len(features))

    for index, item in enumerate(features, start=1):
        print("")
        print(f"----- Sentinel-2 Product {index} -----")
        print("ID:", item.get("id"))
        print("Collection:", item.get("collection"))

        properties = item.get("properties", {})

        print("Datetime:", properties.get("datetime"))
        print(
            "Cloud cover:",
            properties.get("eo:cloud_cover")
        )

except Exception as e:
    print("")
    print("STAC search failed.")
    print("Error type:", type(e).__name__)
    print("Error:", str(e))

print("")
print("===== Test Finished =====")
