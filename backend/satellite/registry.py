"""
GeoShield AI Enterprise
Satellite Registry

Central registry for all satellite and Earth-observation
data providers used by GeoShield.

Sentinel-2 is currently active.
Other providers are registered as planned/inactive
until their connectors are implemented.
"""

from __future__ import annotations

from typing import Any


SATELLITE_REGISTRY: dict[str, dict[str, Any]] = {

    "sentinel2": {
        "id": "sentinel2",
        "name": "Sentinel-2",
        "provider": "Copernicus Data Space",
        "category": "Optical Multispectral",
        "status": "active",
        "description": (
            "Multispectral Earth observation imagery "
            "for vegetation, agriculture, fire and "
            "environmental intelligence."
        ),
        "capabilities": [
            "True Color",
            "NDVI",
            "NDWI",
            "NBR",
            "Agriculture",
            "Fire Analysis",
            "Change Detection",
        ],
        "endpoint": "/sentinel2",
    },

    "sentinel1": {
        "id": "sentinel1",
        "name": "Sentinel-1",
        "provider": "Copernicus Data Space",
        "category": "SAR Radar",
        "status": "planned",
        "description": (
            "Synthetic Aperture Radar imagery for "
            "flood mapping, surface monitoring and "
            "all-weather Earth observation."
        ),
        "capabilities": [
            "Flood Detection",
            "Surface Monitoring",
            "Change Detection",
            "SAR Analysis",
        ],
        "endpoint": "/sentinel1",
    },

    "viirs": {
        "id": "viirs",
        "name": "VIIRS",
        "provider": "NASA / NOAA",
        "category": "Thermal / Environmental",
        "status": "planned",
        "description": (
            "Near-real-time environmental observations "
            "for fire, thermal anomalies and atmospheric monitoring."
        ),
        "capabilities": [
            "Fire Hotspots",
            "Thermal Anomalies",
            "Nighttime Lights",
            "Environmental Monitoring",
        ],
        "endpoint": "/viirs",
    },

    "gpm": {
        "id": "gpm",
        "name": "GPM",
        "provider": "NASA",
        "category": "Precipitation",
        "status": "planned",
        "description": (
            "Global precipitation observations for "
            "rainfall monitoring and flood intelligence."
        ),
        "capabilities": [
            "Rainfall",
            "Precipitation",
            "Flood Intelligence",
            "Storm Monitoring",
        ],
        "endpoint": "/gpm",
    },

    "era5": {
        "id": "era5",
        "name": "ERA5",
        "provider": "ECMWF / Copernicus",
        "category": "Climate / Weather",
        "status": "planned",
        "description": (
            "Global atmospheric reanalysis data for "
            "weather, climate and environmental intelligence."
        ),
        "capabilities": [
            "Temperature",
            "Wind",
            "Pressure",
            "Humidity",
            "Climate Analysis",
        ],
        "endpoint": "/era5",
    },
}


def get_all_satellites() -> list[dict[str, Any]]:
    """Return every registered satellite provider."""

    return list(SATELLITE_REGISTRY.values())


def get_active_satellites() -> list[dict[str, Any]]:
    """Return only currently active satellite providers."""

    return [
        satellite
        for satellite in SATELLITE_REGISTRY.values()
        if satellite["status"] == "active"
    ]


def get_satellite(satellite_id: str) -> dict[str, Any] | None:
    """Return one satellite by ID."""

    return SATELLITE_REGISTRY.get(satellite_id)


__all__ = [
    "SATELLITE_REGISTRY",
    "get_all_satellites",
    "get_active_satellites",
    "get_satellite",
]
