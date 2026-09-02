import httpx

from core.auth import CopernicusAuthManager

print("===== GEOSHIELD AUTHENTICATED CATALOGUE TEST =====")

manager = CopernicusAuthManager()
token = manager.get_token()

print("Authentication:", "PASS" if token else "FAIL")
print("Token valid:", manager.is_token_valid())

url = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products?%24top=1"

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json",
    "User-Agent": "GeoShield-AI/0.1",
}

try:
    response = httpx.get(
        url,
        headers=headers,
        timeout=60,
    )

    print("HTTP status:", response.status_code)
    print("Response bytes:", len(response.content))

    if response.is_success:
        print("Authenticated catalogue access: PASS")
        print("Response:", response.text[:1000])
    else:
        print("Authenticated catalogue access: FAILED")
        print("Response:", response.text[:2000])

except Exception as exc:
    print("Authenticated catalogue access: ERROR")
    print("Error type:", type(exc).__name__)
    print("Error:", str(exc))

print("================================================")
