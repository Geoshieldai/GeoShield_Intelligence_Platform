from core.data.copernicus_client import CopernicusCatalogueClient

print("===== GEOSHIELD CDSE CLIENT HEALTH CHECK =====")

client = CopernicusCatalogueClient()

try:
    products = client.list_products(limit=1)

    print("CDSE authentication: PASS")
    print("Catalogue transport: PASS")
    print("Catalogue query: PASS")
    print("Products returned:", len(products))

    if products:
        product = products[0]

        print()
        print("First product:")
        print("ID:", product.get("Id"))
        print("Name:", product.get("Name"))
        print("ContentType:", product.get("ContentType"))
        print("S3Path:", product.get("S3Path"))

    print()
    print("GeoShield CDSE client: HEALTHY")

except Exception as exc:
    print("CDSE client health check: FAILED")
    print("Error type:", type(exc).__name__)
    print("Error:", str(exc))

print("===============================================")
