from core.data import CopernicusClient

url = "https://stac.dataspace.copernicus.eu/v1/"

print("===== AUTHENTICATED STAC TEST =====")

try:
    with CopernicusClient() as client:
        response = client.get(url)

        print("HTTP status:", response.status_code)
        print("Response received:", bool(response.content))

        if response.ok:
            print("Authenticated STAC access: SUCCESS")
        else:
            print("Authenticated STAC access: FAILED")
            print("Response:", response.text[:500])

except Exception as exc:
    print("Authenticated STAC access: FAILED")
    print("Error type:", type(exc).__name__)
    print("Error:", str(exc))

print("===== TEST FINISHED =====")
