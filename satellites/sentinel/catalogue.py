"""
Copernicus Catalogue Client

Communicates with the CDSE Catalogue API.
"""

import requests

from satellites.auth.token_manager import TokenManager


CATALOGUE_URL = (
    "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"
)


class CopernicusCatalogue:

    def __init__(self):

        self.token_manager = TokenManager()

    def headers(self):

        token = self.token_manager.get_token()

        return {
            "Authorization": f"Bearer {token}"
        }

    def search(self, params=None):

        response = requests.get(
            CATALOGUE_URL,
            headers=self.headers(),
            params=params,
            timeout=60,
        )

        response.raise_for_status()

        return response.json()