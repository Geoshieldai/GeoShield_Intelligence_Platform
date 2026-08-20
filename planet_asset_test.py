import os
import httpx
from dotenv import load_dotenv

load_dotenv()

PLANET_API_KEY = os.getenv("PLANET_API_KEY", "").strip()
ITEM_ID = "20260812_161454_28_252b"
ITEM_TYPE = "PSScene"

print("===== GeoShield Planet Asset Test =====")
print(f"Planet API key loaded: {bool(PLANET_API_KEY)}")
print(f"Testing item: {ITEM_ID}")
print()

if not PLANET_API_KEY:
    raise RuntimeError("PLANET_API_KEY is not loaded.")

url = f"https://api.planet.com/data/v1/item-types/{ITEM_TYPE}/items/{ITEM_ID}"

print("Requesting Planet item metadata...")
print(f"Endpoint: {url}")
print()

try:
    with httpx.Client(
        auth=(PLANET_API_KEY, ""),
        timeout=60.0,
        http2=False
    ) as client:

        response = client.get(url)

    print(f"HTTP status: {response.status_code}")

    if response.is_success:
        data = response.json()

        print("Planet item metadata: SUCCESS")
        print()

        properties = data.get("properties", {})

        print("===== Product Information =====")
        print(f"ID: {data.get('id')}")
        print(f"Type: {data.get('type')}")
        print(f"Item type: {properties.get('item_type')}")
        print(f"Acquired: {properties.get('acquired')}")
        print(f"Cloud cover: {properties.get('cloud_cover')}")
        print(f"GSD: {properties.get('gsd')}")
        print(f"Satellite ID: {properties.get('satellite_id')}")
        print()

        print("===== Available Assets =====")

        assets = data.get("assets", {})

        print(f"Asset count: {len(assets)}")
        print()

        for asset_name, asset in assets.items():
            print(f"Asset: {asset_name}")
            print(f"Title: {asset.get('title')}")
            print(f"Type: {asset.get('type')}")
            print(f"Status: {asset.get('status')}")
            print(f"Permissions: {asset.get('permissions')}")
            print(f"Location: {asset.get('location')}")
            print()

    else:
        print("Planet API request failed.")
        print(f"Response: {response.text[:1000]}")

except Exception as e:
    print("Planet request failed.")
    print(f"Error type: {type(e).__name__}")
    print(f"Error: {e}")

print("===== Test Finished =====")
