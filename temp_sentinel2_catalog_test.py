from core.connectors.sentinel2.sentinel2_catalog_service import Sentinel2CatalogService


service = Sentinel2CatalogService(timeout=30)

KENYA_BBOX = [
    33.8,
    -4.7,
    41.9,
    5.2,
]


print("BUILDING_REQUEST...")

request = service.build_search_request(
    start_date="2026-08-01",
    end_date="2026-08-10",
    cloud_cover_max=30,
    limit=3,
    bbox=KENYA_BBOX,
)

print("URL:", request["url"])
print("METHOD:", request["method"])
print("COLLECTIONS:", request["json"]["collections"])
print("BBOX:", request["json"]["bbox"])
print("LIMIT:", request["json"]["limit"])

print("SEARCHING_CATALOG...")

products = service.search(
    start_date="2026-08-01",
    end_date="2026-08-10",
    cloud_cover_max=30,
    limit=3,
    bbox=KENYA_BBOX,
)

print("PRODUCT_COUNT:", len(products))

for index, product in enumerate(products, start=1):
    print(
        f"PRODUCT_{index}:",
        product.product_id,
        "| DATE:",
        product.acquisition_date,
        "| CLOUD:",
        product.cloud_cover,
        "| TILE:",
        product.tile_id,
    )
