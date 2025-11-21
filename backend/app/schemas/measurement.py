from typing import Optional
from pydantic import BaseModel
from datetime import datetime as datetime_type


class MeasurementResponseSchema(BaseModel):
    id: int
    source: str
    type: str
    value: float
    unit: str
    datetime: datetime_type
    city_id: int


class MeasurementCreateSchema(BaseModel):
    source: str
    type: str
    value: float
    unit: str
    datetime: datetime_type
    city_id: int


class MeasurementUpdateSchema(BaseModel):
    source: Optional[str] = None
    type: Optional[str] = None
    value: Optional[float] = None
    unit: Optional[str] = None
    datetime: Optional[datetime_type] = None
    city_id: Optional[int] = None
