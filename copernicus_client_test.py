"""
GeoShield AI Enterprise
CDSE Authenticated Catalogue Test
"""

from core.data import CopernicusClient
from core.config import settings


def main() -> None:

    print("===== GEOSHIELD CDSE CLIENT TEST =====")

    url = settings.cdse_catalog_url

    params = {
        "$filter": "Collection/Name eq 'SENTINEL-2'",
        "$top": 3,
    }

    print("Catalogue endpoint:", url)
    print("Authentication source: CopernicusAuthManager")
    print("Credentials exposed: NO")

    try:

        with CopernicusClient() as client:

            response = client.get(
                url,
                params=params,
            )

            print("HTTP status:", response.status_code)

            response.raise_for_status()

            data = response.json()

            products = data.get("value", [])

            print("Catalogue access: SUCCESS")
            print("Products returned:", len(products))

            for index, product in enumerate(
                products,
                start=1,
            ):

                print()
                print(f"----- Product {index} -----")
                print("Name:", product.get("Name"))
                print("ID:", product.get("Id"))

    except Exception as exc:

        print("Catalogue access: FAILED")
        print("Error type:", type(exc).__name__)
        print("Error:", str(exc))

    print()
    print("===== TEST FINISHED =====")


if __name__ == "__main__":
    main()
