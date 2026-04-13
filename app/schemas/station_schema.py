from pydantic import BaseModel
from typing import Optional

class StoreSchema(BaseModel):
    codigo: Optional[str]
    nombre: Optional[str]
    tipo: Optional[str]


class StationDataSchema(BaseModel):
    id: str
    compania: str
    direccion: str
    comuna: str
    region: str
    latitud: float
    longitud: float
    distancia_lineal: float
    precio: Optional[int]
    tiene_tienda: bool
    tienda: Optional[StoreSchema]


class StationResponse(BaseModel):
    success: bool
    data: StationDataSchema