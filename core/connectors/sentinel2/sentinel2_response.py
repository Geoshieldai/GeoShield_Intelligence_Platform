"""
GeoShield Sentinel-2 Response

Standardized response object for Sentinel-2 provider operations.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Sentinel2Response:
    """
    Standard response returned by the Sentinel-2 client.
    """

    is_successful: bool
    operation: str
    provider: str
    data: dict[str, Any] | None = None
    error: str | None = None

    @property
    def success(self) -> bool:
        """
        Compatibility property used by the test suite and callers.

        Returns True when the operation was successful.
        """
        return self.is_successful

    @classmethod
    def success_response(
        cls,
        operation: str,
        provider: str,
        data: dict[str, Any] | None = None,
    ) -> "Sentinel2Response":
        """
        Create a successful response.

        The method is named success_response to avoid conflicting
        with the success property.
        """
        return cls(
            is_successful=True,
            operation=operation,
            provider=provider,
            data=data or {},
            error=None,
        )

    @classmethod
    def failure(
        cls,
        operation: str,
        provider: str,
        error: str,
    ) -> "Sentinel2Response":
        """
        Create a failed response.
        """
        return cls(
            is_successful=False,
            operation=operation,
            provider=provider,
            data={},
            error=error,
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the response into a dictionary.
        """
        return {
            "success": self.is_successful,
            "operation": self.operation,
            "provider": self.provider,
            "data": self.data or {},
            "error": self.error,
        }