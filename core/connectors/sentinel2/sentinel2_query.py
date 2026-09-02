"""
GeoShield Sentinel-2 Query Builder

Converts a Sentinel2Request into provider-compatible
query parameters.

No network communication occurs here.
"""

from __future__ import annotations

from typing import Any

from .sentinel2_request import Sentinel2Request


class Sentinel2Query:
    """
    Build a provider-ready Sentinel-2 catalog query.
    """

    def __init__(self, request: Sentinel2Request) -> None:
        self.request = request

    def validate(self) -> bool:
        """
        Validate the underlying request.
        """
        return self.request.validate()

    def to_params(self) -> dict[str, Any]:
        """
        Convert the request into catalog query parameters.
        """

        if not self.validate():
            raise ValueError("Invalid Sentinel-2 request.")

        params: dict[str, Any] = {
            "startDate": self.request.start_date,
            "completionDate": self.request.end_date,
        }

        if self.request.cloud_cover_max is not None:
            params["cloudCover"] = self.request.cloud_cover_max

        if self.request.tile_id:
            params["tileId"] = self.request.tile_id

        if self.request.bbox:
            params["bbox"] = ",".join(
                str(value) for value in self.request.bbox
            )

        return params

    def to_dict(self) -> dict[str, Any]:
        """
        Return the query representation.
        """
        return self.to_params()