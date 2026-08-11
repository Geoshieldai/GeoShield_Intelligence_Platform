"""
GeoShield Satellite Search Engine

Coordinates searches across all satellite providers.
"""

from satellites.sentinel.search import SentinelSearch
from satellites.landsat.search import LandsatSearch
from satellites.modis.search import MODISSearch
from satellites.viirs.search import VIIRSSearch


class SatelliteSearchEngine:
    """
    Unified search engine for all satellite providers.
    """

    def __init__(self):

        self.providers = {
            "Sentinel": SentinelSearch(),
            "Landsat": LandsatSearch(),
            "MODIS": MODISSearch(),
            "VIIRS": VIIRSSearch(),
        }

    def search_all(
        self,
        latitude,
        longitude,
        start_date,
        end_date,
        cloud_cover=20,
        limit=10,
    ):
        """
        Search every registered provider.
        """

        results = []

        for name, provider in self.providers.items():

            try:

                provider_results = provider.search(
                    latitude=latitude,
                    longitude=longitude,
                    start_date=start_date,
                    end_date=end_date,
                    cloud_cover=cloud_cover,
                    limit=limit,
                )

                results.extend(provider_results)

            except Exception as error:

                print(f"{name} search failed: {error}")

        return results

    def available_providers(self):

        return list(self.providers.keys())