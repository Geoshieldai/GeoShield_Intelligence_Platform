"""
MODIS Search Provider
"""


class MODISSearch:
    """
    MODIS satellite search provider.
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
                "provider": "MODIS",
                "product_id": "MODIS_TEST_001",
                "date": start_date,
                "cloud_cover": cloud_cover,
                "resolution": "250 m",
                "latitude": latitude,
                "longitude": longitude,
            }
        ]