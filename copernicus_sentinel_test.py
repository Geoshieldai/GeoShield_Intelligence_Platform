import os
import requests

print("===== GeoShield Sentinel-2 Catalogue Test =====")

client_id = os.getenv("COPERNICUS_CLIENT_ID")
client_secret = os.getenv("COPERNICUS_CLIENT_SECRET")

token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"

token_response = requests.post(
    token_url,
    data={
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    },
    timeout=30,
)

if not token_response.ok:
    print("Authentication failed.")
    print(token_response.text[:500])
    raise SystemExit(1)

access_token = token_response.json()["access_token"]

print("Copernicus authentication: SUCCESS")
print("Access token received: True")

catalogue_url = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"

params = {
    "$filter": "Collection/Name eq 'SENTINEL-2' and OData.CSC.Intersects(area=geography'SRID=4326;POLYGON((36.7 -1.4, 36.9 -1.4, 36.9 -1.2, 36.7 -1.2, 36.7 -1.4))')",
    "$top": 5,
    "$orderby": "ContentDate/Start desc",
}

headers = {
    "Authorization": f"Bearer {access_token}",
}

print("Searching Copernicus catalogue...")
print("Area: Nairobi region")
print("Product type: Sentinel-2")
print("Maximum results: 5")

response = requests.get(
    catalogue_url,
    params=params,
    headers=headers,
    timeout=60,
)

print("HTTP status:", response.status_code)

if not response.ok:
    print("Catalogue search failed.")
    print("Response:", response.text[:1000])
    raise SystemExit(1)

data = response.json()
products = data.get("value", [])

print("Catalogue search completed: True")
print("Products found:", len(products))

for i, product in enumerate(products, start=1):
    print()
    print(f"----- Product {i} -----")
    print("Name:", product.get("Name"))
    print("ID:", product.get("Id"))
    print("Collection:", product.get("Collection", {}).get("Name"))
    print("Content date:", product.get("ContentDate", {}).get("Start"))
    print("Online:", product.get("Online"))

print()
print("===== Sentinel-2 Catalogue Test Finished =====")
