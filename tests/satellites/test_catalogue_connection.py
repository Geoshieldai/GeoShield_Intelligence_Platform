import requests

print("\nTesting Copernicus Catalogue...\n")

url = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$top=1"

try:
    response = requests.get(
        url,
        timeout=60,
        verify=True,
    )

    print("Status:", response.status_code)
    print(response.text[:500])

except Exception as e:
    print(type(e).__name__)
    print(e)