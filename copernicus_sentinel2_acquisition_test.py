from core.data.copernicus_client import CopernicusCatalogueClient
from engines.sentinel2.sentinel2_resumable_downloader import (
    authenticate,
    download_product,
)

print("===== GEOSHIELD SENTINEL-2 ACQUISITION TEST =====")

client = CopernicusCatalogueClient()

try:
    print()
    print("STEP 1: Searching Sentinel-2...")

    products = client.search_sentinel2(
        start_date="2026-08-01",
        end_date="2026-08-13",
        limit=10,
        cloud_cover=30,
    )

    print("Search: PASS")
    print("Products found:", len(products))

    if not products:
        raise RuntimeError("No Sentinel-2 products found.")

    # Prefer Sentinel-2 Level-2A products.
    l2a_products = [
        product
        for product in products
        if "MSIL2A" in product.get("Name", "")
    ]

    if not l2a_products:
        raise RuntimeError(
            "No Sentinel-2 L2A products found."
        )

    product = l2a_products[0]

    product_uuid = product.get("Id")
    product_name = product.get("Name")

    if not product_uuid:
        raise RuntimeError(
            "Selected product has no UUID."
        )

    print()
    print("STEP 2: Product selected")
    print("Product:", product_name)
    print("UUID:", product_uuid)

    print()
    print("STEP 3: Authenticating downloader...")

    token = authenticate()

    print("Downloader authentication: PASS")

    print()
    print("STEP 4: Starting Sentinel-2 download...")

    output_file = download_product(
        token,
        product_uuid,
    )

    print()
    print("STEP 5: Acquisition complete")
    print("Downloaded file:", output_file)

    print()
    print("===== GEOSHIELD SENTINEL-2 ACQUISITION: PASS =====")

except Exception as exc:
    print()
    print("===== ACQUISITION FAILED =====")
    print("Error type:", type(exc).__name__)
    print("Error:", str(exc))