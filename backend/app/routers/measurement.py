from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from app.database import Sessionmaker
from app.schemas.measurement import (
    MeasurementResponseSchema,
    MeasurementCreateSchema,
    MeasurementUpdateSchema,
)
from app.crud import measurement as crud
from app.crud import city as crud_city
from app import authentication
from app.schemas.users import UserLoggedInSchema

from datetime import datetime

# utilisation des routers : https://fastapi.tiangolo.com/tutorial/bigger-applications/#another-module-with-apirouter
router = APIRouter(prefix="/measurements", tags=["measurements"])


@router.get("/", response_model=list[MeasurementResponseSchema])
def get_all_measurements(
    user: Annotated[UserLoggedInSchema, Depends(authentication.get_current_user)],
    date_start: datetime | None = Query(None),
    date_end: datetime | None = Query(None),
    departement: int | None = Query(None),
    type: str = Query(None),
    limit: int = Query(500),
    offset: int = Query(0),
):
    with Sessionmaker() as session:
        measurements = crud.get_all_measurements(
            session,
            date_start,
            date_end,
            departement,
            type,
            limit,
            offset,
        )
    if len(measurements) == 0:
        raise HTTPException(
            status_code=404, detail="aucun measurement correspondant aux critères."
        )
    return measurements


@router.get("/{id}", response_model=MeasurementResponseSchema)
def get_measurement_by_id(
    user: Annotated[UserLoggedInSchema, Depends(authentication.get_current_user)],
    id: int,
):
    with Sessionmaker() as session:
        measurement = crud.get_mesurement_by_id(session, id)
        if measurement is None:
            raise HTTPException(status_code=404, detail="le measurement n'existe pas")
    return measurement


@router.post("/", response_model=MeasurementResponseSchema, status_code=201)
def create_measurement(
    user: Annotated[UserLoggedInSchema, Depends(authentication.get_current_user)],
    measurement: MeasurementCreateSchema,
):
    try:
        with Sessionmaker() as session:

            city_db = crud_city.get_city_by_id(session, measurement.city_id)
            if city_db is None:
                raise HTTPException(status_code=404, detail="la ville n'existe pas")

            measurement_db = crud.create_measurement(session, measurement, city_db)
            return measurement_db
    except HTTPException:
        raise
    except Exception as e:
        print(f"exception : {e}")
        raise HTTPException(
            status_code=500, detail=f"Impossible de créer le measurement : " + str(e)
        )


@router.put("/{id}", response_model=MeasurementResponseSchema)
def update_measurement(
    user: Annotated[UserLoggedInSchema, Depends(authentication.get_current_user)],
    id: int,
    measurement: MeasurementUpdateSchema,
):
    try:
        with Sessionmaker() as session:
            measurement = crud.update_measurement(session, id, measurement)
            if measurement is None:
                raise HTTPException(
                    status_code=404, detail="le measurement n'existe pas"
                )
            return measurement
    except Exception as e:
        print(f"exception : {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Impossible de mettre à jour le measurement : " + str(e),
        )


@router.delete("/{id}", response_model=MeasurementResponseSchema)
def delete_measurement(
    user: Annotated[UserLoggedInSchema, Depends(authentication.get_current_user)],
    id: int,
):
    try:
        with Sessionmaker() as session:
            measurement = crud.delete_measurement(session, id)
    except Exception as e:
        print(f"exception : {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Impossible de supprimer le measurement : " + str(e),
        )
    if measurement is None:
        raise HTTPException(status_code=404, detail="le measurement n'existe pas")
    return measurement
