from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from app.database import Sessionmaker
from app.schemas.measurement import MeasurementResponseSchema

from app.crud import measurement as crud
from app import authentication
from app.schemas.users import UserLoggedInSchema

from datetime import datetime

# utilisation des routers : https://fastapi.tiangolo.com/tutorial/bigger-applications/#another-module-with-apirouter
router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/temperature/average")
def stats_temperature(
    user: Annotated[UserLoggedInSchema, Depends(authentication.get_current_user)],
    date_start: datetime | None = Query(None),
    date_end: datetime | None = Query(None),
):
    with Sessionmaker() as session:
        measurements = crud.get_all_measurements_include_city(
            session,
            date_start,
            date_end,
            type="temperature"
        )

    if len(measurements) == 0:
        raise HTTPException(
            status_code=404, detail="aucun measurement correspondant aux critères."
        )

    by_year: dict[str, list] = {}

    final_agg: dict[str, dict[str, float]] = {}

    # on aggrege par année

    for data in measurements:
        dept = data.city.departement
        year = data.datetime.year
        value = data.value

        if not str(year) in by_year:
            by_year[str(year)] = []

        by_year[str(year)].append((dept, value))

    # on aggrege par année et departement

    for year, data in by_year.items():
        if not str(year) in final_agg:
            final_agg[str(year)] = {}

        # on aggrege par département pour l'année year
        by_departement: dict[str, list] = {}
        for dept, value in data:
            if not str(dept) in by_departement:
                by_departement[str(dept)] = []
            by_departement[str(dept)].append(value)

        for dept, items in by_departement.items():
            value = sum(items) / len(items)

            final_agg[str(year)][dept] = value

    return final_agg
