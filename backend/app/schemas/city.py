from typing import Optional
from pydantic import BaseModel


class CityResponseSchema(BaseModel):
    id: int
    code_insee: str
    name: str
    code_postal: int
    departement: int
    lat: float
    lng: float


class CityCreateSchema(BaseModel):
    code_insee: str
    name: str
    code_postal: int
    departement: int
    lat: float
    lng: float


class CityUpdateSchema(BaseModel):
    code_insee: Optional[str] = None
    name: Optional[str] = None
    code_postal: Optional[int] = None
    departement: Optional[int] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
