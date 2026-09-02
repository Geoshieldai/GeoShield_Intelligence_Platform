import os
import sys
import httpx
from datetime import datetime, timedelta, timezone

# ============================================================
# GEOSHIELD SENTINEL-2 CONNECTOR
# Copernicus Data Space Ecosystem
# ============================================================

TOKEN_URL = (
    "https://identity.dataspace.copernicus.eu/"
    "auth/realms/CDSE/protocol/openid-connect/token"
)

CATALOG_URL = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"

CLIENT_ID = "cdse-public"

USERNAME = os.getenv("CDSE_USERNAME")
PASSWORD = os.getenv("CDSE_PASSWORD")


def authenticate():
    print("===== GEOSHIELD SENTINEL-2 CONNECTOR =====")
    print("Authenticating with Copernicus Data Space...")

    if not USERNAME or not PASSWORD:
        print()
        print("ERROR: CDSE credentials are not set.")
        print()
        print("Set them in PowerShell first:")
        print('$env:CDSE_USERNAME="your_email"')
        print('$env:CDSE_PASSWORD="your_password"')
        sys.exit(1)

    response = httpx.post(
        TOKEN_URL,
        data={
            "grant_type": "password",
            "client_id": CLIENT_ID,
            "username": USERNAME,
            "password": PASSWORD,
        },
        timeout=60,
    )

    print("AUTH:", response.status_code)

    response.raise_for_status()

    token = response.json().get("access_token")

    if not token:
        print("ERROR: Authentication succeeded but no token was returned.")
        sys.exit(1)

    print("TOKEN: True")
    return token


def search_sentinel2(
    token,
    start_date,
    end_date,
    tile="T37MBU",
    cloud_cover=20,
    limit=10,
):
    print()
    print("===== SENTINEL-2 SEARCH =====")
    print("Tile:", tile)
    print("Start:", start_date)
    print("End:", end_date)
    print("Maximum cloud cover:", cloud_cover, "%")

    # Sentinel-2 Level-2A products
    filter_expression = (
        "Collection/Name eq 'SENTINEL-2' "
        "and contains(Name,'MSIL2A') "
        f"and contains(Name,'{tile}') "
        f"and ContentDate/Start gt {start_date}T00:00:00.000Z "
        f"and ContentDate/Start lt {end_date}T23:59:59.999Z "
        f"and Attributes/OData.CSC.DoubleAttribute/any("
        "att:att/Name eq 'cloudCover' "
        f"and att/att/Value le {cloud_cover})"
    )

    params = {
        "$filter": filter_expression,
        "$orderby": "ContentDate/Start desc",
        "$top": limit,
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    response = httpx.get(
        CATALOG_URL,
        params=params,
        headers=headers,
        timeout=120,
    )

    print("CATALOG HTTP:", response.status_code)

    response.raise_for_status()

    products = response.json().get("value", [])

    print("Products found:", len(products))

    return products


def print_products(products):
    print()

    if not products:
        print("No suitable Sentinel-2 products found.")
        return

    print("===== AVAILABLE SENTINEL-2 PRODUCTS =====")

    for index, product in enumerate(products, start=1):
        name = product.get("Name")
        product_id = product.get("Id")
        online = product.get("Online")

        content_date = product.get("ContentDate", {})
        acquisition = content_date.get("Start")

        print()
        print(f"[{index}]")
        print("Name:", name)
        print("UUID:", product_id)
        print("Acquisition:", acquisition)
        print("Online:", online)


def main():
    token = authenticate()

    today = datetime.now(timezone.utc).date()

    # Search the previous 30 days automatically.
    start_date = today - timedelta(days=30)
    end_date = today

    products = search_sentinel2(
        token=token,
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat(),
        tile="T37MBU",
        cloud_cover=20,
        limit=10,
    )

    print_products(products)

    print()
    print("===== CONNECTOR STATUS =====")

    if products:
        print("Sentinel-2 connection: READY")
        print("Automatic scene discovery: READY")
    else:
        print("Sentinel-2 connection: AUTHENTICATED")
        print("Automatic scene discovery: NO PRODUCTS FOUND")

    print()
    print("SENTINEL-2 CONNECTOR COMPLETE")


if __name__ == "__main__":
    main()
