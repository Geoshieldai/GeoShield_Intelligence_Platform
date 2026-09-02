"""
VIIRS Search Provider
"""


class VIIRSSearch:
    """
    VIIRS satellite search provider.
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
                "provider": "VIIRS",
                "product_id": "VIIRS_TEST_001",
                "date": start_date,
                "cloud_cover": cloud_cover,
                "resolution": "375 m",
                "latitude": latitude,
                "longitude": longitude,
            }
        ]