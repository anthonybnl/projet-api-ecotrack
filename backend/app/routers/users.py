from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas.users import (
    UserCreateSchema,
    UserLoggedInSchema,
    UserLoginSchema,
    UserResponseSchema,
    UserUpdateSchema,
)
from app.database import Sessionmaker
from app.crud import users as crud
from app import authentication

# utilisation des routers : https://fastapi.tiangolo.com/tutorial/bigger-applications/#another-module-with-apirouter
router = APIRouter(tags=["users"])


@router.post("/register", response_model=UserResponseSchema, status_code=201)
def create_user(user: UserCreateSchema):
    try:
        with Sessionmaker() as session:
            if crud.check_if_user_already_exists(session, user.email):
                raise HTTPException(
                    status_code=409,
                    detail="un user avec le même email existe déja.",
                )
            user_in_db = crud.create_user(session, user)
            return user_in_db
    except HTTPException:
        raise
    except Exception as e:
        print(f"exception : {e}")
        raise HTTPException(
            status_code=500, detail=f"Impossible de créer l'utilisateur : " + str(e)
        )


@router.post("/login", response_model=dict)
def login(user: UserLoginSchema) -> bool:
    try:
        with Sessionmaker() as session:
            db_user = crud.login(session, user.email, user.password)
            if db_user is not None:
                token = authentication.generate_jwt(db_user.email, db_user.role)
                return {"access_token": token}
            else:
                raise HTTPException(
                    status_code=401,
                    detail="Impossible d'authentifier l'utilisateur",
                )
    except Exception:
        raise


@router.get("/whoami")
def whoami(
    user: Annotated[UserLoggedInSchema, Depends(authentication.get_current_user)],
):
    return user


############## crud pour les admin ##############""


@router.get("/users")
def whoami(
    user: Annotated[UserLoggedInSchema, Depends(authentication.get_current_admin_user)],
    limit: int = Query(10),
    offset: int = Query(0),
):
    with Sessionmaker() as session:
        res = crud.get_users(session, limit, offset)
        return res


@router.put("/users/{id}", response_model=UserResponseSchema)
def update_user(
    id: int,
    user: UserUpdateSchema,
):
    try:
        with Sessionmaker() as session:
            city = crud.update_user(session, id, user)
            if city is None:
                raise HTTPException(status_code=404, detail="le user n'existe pas")
            return city
    except Exception as e:
        print(f"exception : {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Impossible de mettre à jour l'utilisateur : " + str(e),
        )
