import httpx

print("===== GeoShield Sentinel-2 Asset Inspection =====")

PRODUCT_ID = "S2A_MSIL2A_20260812T074031_N0512_R092_T37MBU_20260812T125812"

URL = (
    "https://stac.dataspace.copernicus.eu/v1/"
    f"collections/sentinel-2-l2a/items/{PRODUCT_ID}"
)

print("Product:")
print(PRODUCT_ID)
print("")
print("Requesting product metadata...")
print("")

try:
    response = httpx.get(
        URL,
        timeout=60,
    )

    print("HTTP status:", response.status_code)

    response.raise_for_status()

    item = response.json()

    print("Product metadata: SUCCESS")

    print("")
    print("===== Product Information =====")
    print("ID:", item.get("id"))
    print("Collection:", item.get("collection"))

    properties = item.get("properties", {})

    print("Datetime:", properties.get("datetime"))
    print("Cloud cover:", properties.get("eo:cloud_cover"))

    assets = item.get("assets", {})

    print("")
    print("===== Available Assets =====")
    print("Asset count:", len(assets))

    for name, asset in assets.items():
        print("")
        print("Asset:", name)
        print("Title:", asset.get("title"))
        print("Type:", asset.get("type"))
        print("Roles:", asset.get("roles"))
        print("Resolution:", asset.get("gsd"))
        print("")

except Exception as e:
    print("")
    print("Asset inspection failed.")
    print("Error type:", type(e).__name__)
    print("Error:", str(e))

print("")
print("===== Test Finished =====")
