"""
Sentinel Search Filters
"""


class SentinelFilters:

    @staticmethod
    def cloud(max_cloud):

        return (
            f"Attributes/OData.CSC.DoubleAttribute/"
            f"any(att:att/Name eq 'cloudCover' "
            f"and att/OData.CSC.DoubleAttribute/Value le {max_cloud})"
        )