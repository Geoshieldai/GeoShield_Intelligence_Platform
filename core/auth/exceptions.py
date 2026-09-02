"""
GeoShield AI Enterprise
Copernicus Authentication Exceptions
"""

from __future__ import annotations


class CopernicusAuthError(Exception):
    """Base authentication error."""


class CopernicusConfigurationError(CopernicusAuthError):
    """Raised when required authentication configuration is missing."""


class CopernicusAuthenticationError(CopernicusAuthError):
    """Raised when Copernicus rejects authentication."""


class CopernicusNetworkError(CopernicusAuthError):
    """Raised when Copernicus cannot be reached."""
