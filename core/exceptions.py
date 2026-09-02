"""
Platform Exceptions
"""


class GeoShieldException(Exception):
    """Base exception for GeoShield."""


class ConfigurationError(GeoShieldException):
    """Configuration error."""


class DatabaseError(GeoShieldException):
    """Database error."""


class SatelliteError(GeoShieldException):
    """Satellite processing error."""


class AIModelError(GeoShieldException):
    """AI model error."""