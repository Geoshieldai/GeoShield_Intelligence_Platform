"""
GeoShield Data Normalizer

Provides basic normalization of incoming observation
and dataset values before analysis.
"""

from typing import Any


class DataNormalizer:
    """
    Normalizes incoming data into predictable structures.
    """

    def normalize_observation(
        self,
        observation: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Normalize an observation dictionary.
        """

        normalized = dict(observation)

        if "latitude" in normalized:
            normalized["latitude"] = float(normalized["latitude"])

        if "longitude" in normalized:
            normalized["longitude"] = float(normalized["longitude"])

        return normalized

    def normalize_values(
        self,
        values: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Normalize numeric values to floats where possible.
        """

        normalized: dict[str, Any] = {}

        for key, value in values.items():
            if isinstance(value, bool):
                normalized[key] = value
                continue

            if isinstance(value, (int, float)):
                normalized[key] = float(value)
                continue

            normalized[key] = value

        return normalized