import requests

print("===== Copernicus Catalogue Connection Test =====")

url = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"

params = {
    "$filter": "Collection/Name eq 'SENTINEL-2'",
    "$top": 3,
}

print("Testing Copernicus catalogue...")
print("Endpoint:", url)

try:
    response = requests.get(
        url,
        params=params,
        timeout=60,
    )

    print("HTTP status:", response.status_code)
    print("Response received:", bool(response.text))
    print("Final URL:", response.url)

    if response.ok:
        data = response.json()
        products = data.get("value", [])

        print("Catalogue connection: SUCCESS")
        print("Products returned:", len(products))

        for i, product in enumerate(products, start=1):
            print()
            print(f"----- Product {i} -----")
            print("Name:", product.get("Name"))
            print("ID:", product.get("Id"))

    else:
        print("Catalogue request failed.")
        print("Response:", response.text[:1000])

except Exception as e:
    print("Catalogue connection failed.")
    print("Error type:", type(e).__name__)
    print("Error:", str(e))

print()
print("===== Test Finished =====")
