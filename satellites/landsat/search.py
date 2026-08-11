"""
Landsat Search Provider
"""


class LandsatSearch:
    """
    Landsat satellite search provider.
    """

    def search(
        self,
        latitude,
        longitude,
        start_date,
        end_date,
        cloud_cover=20,
        limit=10,
    ):

        return [
            {
                "provider": "Landsat",
                "product_id": "LS_TEST_001",
                "date": start_date,
                "cloud_cover": cloud_cover,
                "resolution": "30 m",
                "latitude": latitude,
                "longitude": longitude,
            }
        ]