from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from app.database import Sessionmaker
from app.schemas.city import CityCreateSchema, CityResponseSchema, CityUpdateSchema
from app.crud import city as crud
from app import authentication
from app.schemas.users import UserLoggedInSchema

# utilisation des routers : https://fastapi.tiangolo.com/tutorial/bigger-applications/#another-module-with-apirouter
router = APIRouter(prefix="/cities", tags=["cities"])


@router.get("/", response_model=list[CityResponseSchema])
def get_all_cities(
    user: Annotated[UserLoggedInSchema, Depends(authentication.get_current_user)],
):
    with Sessionmaker() as session:
        movies = crud.get_all_cities(session)
    if len(movies) == 0:
        raise HTTPException(
            status_code=404, detail="aucun ville correspondant aux critères."
        )
    return movies


@router.get("/{id}", response_model=CityResponseSchema)
def get_city_by_id(
    user: Annotated[UserLoggedInSchema, Depends(authentication.get_current_user)],
    id: int,
):
    with Sessionmaker() as session:
        movie = crud.get_city_by_id(session, id)
        if movie is None:
            raise HTTPException(status_code=404, detail="La ville n'existe pas")
    return movie


@router.post("/", response_model=CityResponseSchema, status_code=201)
def create_city(
    user: Annotated[UserLoggedInSchema, Depends(authentication.get_current_user)],
    city: CityCreateSchema,
):
    try:
        with Sessionmaker() as session:

            db_city_same_code_insee = crud.get_city_by_code_insee(
                session, city.code_insee
            )
            if db_city_same_code_insee is not None:
                raise HTTPException(
                    status_code=409,
                    detail="une ville avec le même code INSEE existe déjà",
                )

            db_city_same_code_postal = crud.get_city_by_code_postal(
                session, city.code_postal
            )
            if db_city_same_code_postal is not None:
                raise HTTPException(
                    status_code=409,
                    detail="une ville avec le même code postal existe déjà",
                )
            city_db = crud.create_city(session, city)
            return city_db
    except HTTPException:
        raise
    except Exception as e:
        print(f"exception : {e}")
        raise HTTPException(
            status_code=500, detail=f"Impossible de créer la ville : " + str(e)
        )


@router.put("/{id}", response_model=CityResponseSchema)
def update_city(
    user: Annotated[UserLoggedInSchema, Depends(authentication.get_current_user)],
    id: int,
    city: CityUpdateSchema,
):
    try:
        with Sessionmaker() as session:
            city = crud.update_city(session, id, city)
            if city is None:
                raise HTTPException(status_code=404, detail="la ville n'existe pas")
            return city
    except Exception as e:
        print(f"exception : {e}")
        raise HTTPException(
            status_code=500, detail=f"Impossible de mettre à jour la ville : " + str(e)
        )


@router.delete("/{id}", response_model=CityResponseSchema)
def delete_city(
    user: Annotated[UserLoggedInSchema, Depends(authentication.get_current_user)],
    id: int,
):
    try:
        with Sessionmaker() as session:
            city = crud.delete_city(session, id)
    except Exception as e:
        print(f"exception : {e}")
        raise HTTPException(
            status_code=500, detail=f"Impossible de supprimer la ville : " + str(e)
        )
    if city is None:
        raise HTTPException(status_code=404, detail="la ville n'existe pas")
    return city
