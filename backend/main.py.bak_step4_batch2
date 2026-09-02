from backend.routes.dashboard import router as dashboard_router
from backend.routes.county import router as county_router
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import asyncio
from contextlib import asynccontextmanager
from backend.services.ai_center import ai_loop

from backend.routes.health import router as health_router
from backend.routes.resources import router as resources_router
from backend.routes.alerts import router as alerts_router

from backend.api.satellite import router as satellite_router

@asynccontextmanager
async def lifespan(app):

    asyncio.create_task(ai_loop())

    yield


app = FastAPI(

    title="GeoShield AI",

    version="1.0",

    lifespan=lifespan

)

app.include_router(health_router)
app.include_router(county_router)
app.include_router(dashboard_router)
app.include_router(resources_router)
app.include_router(alerts_router)

app.include_router(
    satellite_router,
    prefix="/satellite",
    tags=["Satellite"]
)

app.mount(
    "/static",
    StaticFiles(directory="frontend/static"),
    name="static"
)


@app.get("/")
def home():
    return FileResponse("frontend/templates/index.html")