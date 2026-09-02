"""
GeoShield Data Validator

Validates basic geospatial observations before they
enter the GeoShield processing pipeline.
"""

from typing import Any


class DataValidator:
    """
    Performs basic validation of incoming geospatial data.
    """

    def validate_coordinates(
        self,
        latitude: float,
        longitude: float,
    ) -> bool:
        """
        Validate latitude and longitude ranges.
        """

        if not -90 <= latitude <= 90:
            return False

        if not -180 <= longitude <= 180:
            return False

        return True

    def validate_observation(
        self,
        observation: dict[str, Any],
    ) -> bool:
        """
        Validate the minimum required observation fields.
        """

        required_fields = {
            "observation_id",
            "latitude",
            "longitude",
            "timestamp",
            "source",
        }

        if not required_fields.issubset(observation):
            return False

        try:
            latitude = float(observation["latitude"])
            longitude = float(observation["longitude"])
        except (TypeError, ValueError):
            return False

        return self.validate_coordinates(latitude, longitude)