"""
GeoShield AI Enterprise
Legacy Satellite API Compatibility Layer

IMPORTANT:
The former implementation depended directly on the Planet SDK.

Planet is NOT part of the active Sentinel-2 architecture.

The Planet integration is retained in backend/satellite/ for
legacy/reference purposes, but this API no longer imports it.

Active satellite imagery is being migrated to the
Copernicus Data Space / Sentinel-2 API.
"""

from fastapi import APIRouter, HTTPException


router = APIRouter()


@router.get("/latest")
async def latest_images():
    """
    Legacy Planet endpoint.

    Planet is intentionally disabled.

    Sentinel-2 imagery is now handled by the dedicated
    /api/sentinel2 endpoints.
    """

    raise HTTPException(
        status_code=410,
        detail={
            "status": "disabled",
            "provider": "Planet",
            "message": (
                "The legacy Planet imagery service is disabled. "
                "Use the Sentinel-2 Copernicus service."
            ),
        },
    )


@router.get("/assets/{scene_id}")
async def scene_assets(scene_id: str):
    """
    Legacy Planet asset endpoint.

    Kept only for API compatibility.
    """

    raise HTTPException(
        status_code=410,
        detail={
            "status": "disabled",
            "provider": "Planet",
            "scene_id": scene_id,
            "message": (
                "Planet asset access is disabled. "
                "Use Sentinel-2 imagery assets."
            ),
        },
    )


@router.get("/latest-scene")
async def latest_scene():
    """
    Legacy Planet latest-scene endpoint.

    Kept only for API compatibility.
    """

    raise HTTPException(
        status_code=410,
        detail={
            "status": "disabled",
            "provider": "Planet",
            "message": (
                "Planet latest-scene access is disabled. "
                "Use the Sentinel-2 service."
            ),
        },
    )
