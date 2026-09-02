"""
GeoShield AI Enterprise
Sentinel-2 API
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from core.data.copernicus_client import CopernicusCatalogueClient


router = APIRouter()


@router.get("/search")
def search_sentinel2(
    bbox: str | None = Query(
        None,
        description="Bounding box: west,south,east,north",
    ),
    date_from: str = Query(
        ...,
        description="Start date in YYYY-MM-DD format",
    ),
    date_to: str = Query(
        ...,
        description="End date in YYYY-MM-DD format",
    ),
    cloud_cover: float | None = Query(
        20.0,
        ge=0,
        le=100,
        description="Maximum cloud cover percentage",
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Maximum number of Sentinel-2 products",
    ),
):
    """
    Search the Copernicus Data Space catalogue for Sentinel-2 products.

    The frontend contract uses:
        bbox
        date_from
        date_to
        cloud_cover
        limit
    """

    try:
        client = CopernicusCatalogueClient()

        products = client.search_sentinel2(
            start_date=date_from,
            end_date=date_to,
            limit=limit,
            cloud_cover=cloud_cover,
            bbox=bbox,
        )

        return {
            "status": "success",
            "source": "Copernicus Data Space",
            "product_type": "Sentinel-2",
            "count": len(products),
            "products": products,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail={
                "status": "error",
                "source": "Copernicus Data Space",
                "message": "Unable to query Sentinel-2 catalogue.",
                "error_type": type(exc).__name__,
            },
        ) from exc


@router.get("/status")
def sentinel2_status():
    """
    Return Sentinel-2 API status information.
    """

    return {
        "status": "online",
        "service": "GeoShield Sentinel-2 API",
        "provider": "Copernicus Data Space",
        "product": "Sentinel-2",
    }
