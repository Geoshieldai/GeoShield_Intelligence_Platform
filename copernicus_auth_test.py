import os
import requests

print("===== GeoShield Copernicus OAuth Test =====")

client_id = os.getenv("COPERNICUS_CLIENT_ID")
client_secret = os.getenv("COPERNICUS_CLIENT_SECRET")

print("Client ID loaded:", bool(client_id))
print("Client Secret loaded:", bool(client_secret))

token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"

payload = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
}

print("Requesting Copernicus access token...")

try:
    response = requests.post(
        token_url,
        data=payload,
        timeout=30,
    )

    print("HTTP status:", response.status_code)

    if response.ok:
        data = response.json()

        print("Copernicus authentication: SUCCESS")
        print("Access token received:", bool(data.get("access_token")))
        print("Token type:", data.get("token_type"))
        print("Expires in:", data.get("expires_in"), "seconds")
    else:
        print("Copernicus authentication: FAILED")
        print("Response:", response.text[:500])

except Exception as e:
    print("Copernicus request failed:", type(e).__name__)
    print("Error:", str(e))
