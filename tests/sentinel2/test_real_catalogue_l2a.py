from core.data.copernicus_client import CopernicusCatalogueClient


client = CopernicusCatalogueClient()

products = client._get(
    {
        "$filter": (
            "Collection/Name eq 'SENTINEL-2' "
            "and "
            "Attributes/OData.CSC.StringAttribute/any("
            "att:att/Name eq 'productType' and "
            "att/OData.CSC.StringAttribute/Value eq 'S2MSI2A'"
            ") "
            "and "
            "ContentDate/Start gt 2026-08-12T06:00:00.000Z "
            "and "
            "ContentDate/Start lt 2026-08-12T08:00:00.000Z"
        ),
        "$top": "20",
        "$orderby": "ContentDate/Start asc",
    }
)

print()
print("============================================================")
print("GEOSHIELD REAL SENTINEL-2 L2A CATALOGUE TEST")
print("============================================================")
print()
print("COUNT:", len(products))

for index, product in enumerate(products, start=1):

    print()
    print(f"--- PRODUCT {index} ---")
    print("ID:", product.get("Id"))
    print("NAME:", product.get("Name"))
    print("CONTENT DATE:", product.get("ContentDate"))
    print("SIZE:", product.get("ContentLength"))
    print("ONLINE:", product.get("Online"))
    print("S3 PATH:", product.get("S3Path"))

    footprint = product.get("GeoFootprint")

    if footprint:
        print(
            "GEOMETRY TYPE:",
            footprint.get("type")
        )

        coordinates = footprint.get("coordinates", [])

        if coordinates:
            print(
                "FIRST COORDINATE:",
                coordinates[0][0]
            )

print()
print("============================================================")
print("TEST COMPLETE")
print("============================================================")
