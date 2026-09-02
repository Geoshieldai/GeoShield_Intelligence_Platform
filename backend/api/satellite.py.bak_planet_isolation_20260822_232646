from typing import List

from fastapi import APIRouter

from backend.models.satellite import PlanetScene, LatestScene
from backend.satellite.planet_service import PlanetService

router = APIRouter()

planet = PlanetService()


@router.get("/latest", response_model=List[PlanetScene])
async def latest_images():
    return await planet.latest_images(limit=100)


@router.get("/assets/{scene_id}", response_model=list[str])
async def scene_assets(scene_id: str):
    return await planet.scene_assets(scene_id)


@router.get("/latest-scene", response_model=LatestScene)
async def latest_scene():
    return await planet.latest_scene_assets()