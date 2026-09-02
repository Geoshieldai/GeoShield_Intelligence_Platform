"""
GeoShield AI Enterprise
Sentinel-2 API

Active satellite imagery API backed by the
Copernicus Data Space Ecosystem.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from core.data.copernicus_client import CopernicusCatalogueClient


router = APIRouter()


@router.get("/search")
def search_sentinel2(
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD format"),
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Maximum number of Sentinel-2 products",
    ),
    cloud_cover: float | None = Query(
        20.0,
        ge=0,
        le=100,
        description="Maximum cloud cover percentage",
    ),
):
    """
    Search the Copernicus Data Space catalogue for Sentinel-2 products.
    """

    try:
        client = CopernicusCatalogueClient()

        products = client.search_sentinel2(
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            cloud_cover=cloud_cover,
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
