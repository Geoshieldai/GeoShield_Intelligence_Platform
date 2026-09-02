from core.data.copernicus_client import CopernicusCatalogueClient

print("===== GEOSHIELD SENTINEL-2 SEARCH TEST =====")

client = CopernicusCatalogueClient()

try:
    products = client.search_sentinel2(
        start_date="2026-08-01",
        end_date="2026-08-13",
        limit=5,
        cloud_cover=30,
    )

    print("Sentinel-2 search: PASS")
    print("Products found:", len(products))

    for i, product in enumerate(products, start=1):
        print()
        print(f"----- Sentinel-2 Product {i} -----")
        print("ID:", product.get("Id"))
        print("Name:", product.get("Name"))
        print("S3Path:", product.get("S3Path"))
        print("ContentDate:", product.get("ContentDate"))

        attributes = product.get("Attributes", [])

        if isinstance(attributes, list):
            for attribute in attributes:
                name = attribute.get("Name")
                value = attribute.get("Value")

                if name and "Cloud" in name:
                    print("Cloud:", value)

    print()
    print("GeoShield Sentinel-2 search: HEALTHY")

except Exception as exc:
    print("Sentinel-2 search: FAILED")
    print("Error type:", type(exc).__name__)
    print("Error:", str(exc))

print("============================================")
