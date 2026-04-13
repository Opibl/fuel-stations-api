from fastapi import FastAPI
from app.api.routes.stations import router as stations_router

app = FastAPI(
    title="Fuel Stations API",
    version="1.0.0",
    description="API para búsqueda de estaciones de combustible"
)

app.include_router(
    stations_router,
    prefix="/api/stations",
    tags=["Stations"]
)