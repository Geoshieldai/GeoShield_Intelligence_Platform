"""
Sentinel Search Provider

Searches the Copernicus Data Space Ecosystem Catalogue.
"""

import requests

from satellites.auth.token_manager import TokenManager


CATALOGUE_URL = (
    "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"
)


class SentinelSearch:

    def __init__(self):

        self.token_manager = TokenManager()

    def search(
        self,
        latitude,
        longitude,
        start_date,
        end_date,
        cloud_cover=20,
        limit=10,
    ):

        token = self.token_manager.get_token()

        headers = {
            "Authorization": f"Bearer {token}"
        }

        params = {
            "$top": limit
        }

        response = requests.get(
            CATALOGUE_URL,
            headers=headers,
            params=params,
            timeout=60,
        )

        response.raise_for_status()

        products = response.json().get("value", [])

        results = []

        for product in products:

            results.append(
                {
                    "provider": "Sentinel",
                    "product_id": product.get("Id"),
                    "name": product.get("Name"),
                }
            )

        return results