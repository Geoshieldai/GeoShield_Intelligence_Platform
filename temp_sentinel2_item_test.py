from core.connectors.sentinel2.sentinel2_catalog_service import Sentinel2CatalogService


service = Sentinel2CatalogService(timeout=30)

KENYA_BBOX = [
    33.8,
    -4.7,
    41.9,
    5.2,
]


request = service.build_search_request(
    start_date="2026-08-10",
    end_date="2026-08-10",
    cloud_cover_max=30,
    limit=1,
    bbox=KENYA_BBOX,
)

token = service._get_access_token()

import requests

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
}

response = requests.post(
    request["url"],
    json=request["json"],
    headers=headers,
    timeout=30,
)

print("HTTP_STATUS:", response.status_code)

response.raise_for_status()

payload = response.json()

features = payload.get("features", [])

print("FEATURE_COUNT:", len(features))

if not features:
    print("NO_FEATURES_RETURNED")
    raise SystemExit(0)

item = features[0]

print("ITEM_ID:", item.get("id"))
print("ITEM_TYPE:", item.get("type"))

print("\nPROPERTIES:")
for key, value in item.get("properties", {}).items():
    print(f"{key}: {value}")

print("\nASSETS:")
for name, asset in item.get("assets", {}).items():
    print(f"ASSET_NAME: {name}")
    print("  HREF:", asset.get("href"))
    print("  TITLE:", asset.get("title"))
    print("  TYPE:", asset.get("type"))
    print("  ROLES:", asset.get("roles"))
    print()
