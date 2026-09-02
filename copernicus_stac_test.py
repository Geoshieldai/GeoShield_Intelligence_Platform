from pystac_client import Client

print("===== GeoShield Copernicus STAC Test =====")

STAC_URL = "https://stac.dataspace.copernicus.eu/v1/"

print("Connecting to Copernicus STAC...")
print("Endpoint:", STAC_URL)

try:
    catalog = Client.open(STAC_URL)

    print("STAC connection: SUCCESS")
    print("Catalog title:", catalog.title)

    print()
    print("Searching Sentinel-2 L2A collections...")

    search = catalog.search(
        collections=["sentinel-2-l2a"],
        max_items=5,
    )

    items = list(search.items())

    print("STAC search completed: True")
    print("Products found:", len(items))

    for i, item in enumerate(items, start=1):
        print()
        print(f"----- Product {i} -----")
        print("ID:", item.id)
        print("Date:", item.datetime)
        print("Collection:", item.collection_id)

except Exception as e:
    print("STAC test failed.")
    print("Error type:", type(e).__name__)
    print("Error:", str(e))

print()
print("===== STAC Test Finished =====")
