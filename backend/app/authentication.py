from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime
from app.schemas.users import UserLoggedInSchema
from app.database import Sessionmaker
from app.crud import users as crud

secret = "thisismysecret"
alqgorithm = "HS256"
issuer = "http://localhost:8000/"
life_second = 3600

# JWT


def generate_jwt(email: str, role: str) -> str:
    jwt_str = jwt.encode(
        {
            "sub": email,
            "iss": issuer,
            "iat": int(datetime.now().timestamp()),
            "exp": int(datetime.now().timestamp() + life_second),
        },
        secret,
        algorithm=alqgorithm,
    )
    return jwt_str


def decode_jwt(token: str):
    res = jwt.decode(
        token,
        secret,
        algorithms=alqgorithm,
        issuer=issuer,
    )
    return res


# FastAPI authentication

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserLoggedInSchema:
    try:
        decoded_jwt = decode_jwt(token)
        email = decoded_jwt["sub"]
        with Sessionmaker() as session:
            user = crud.get_user_by_email(session, email)
            if user is None:
                raise Exception("JWT ok mais user inexistant")
            return UserLoggedInSchema(email=user.email, role=user.role)
    except Exception as e:
        print(f"exception de la récupération de l'utilisateur courant : " + str(e))
        raise HTTPException(
            status_code=401,
            detail="authentification invalide",
        )


def get_current_admin_user(
    user: Annotated[UserLoggedInSchema, Depends(get_current_user)],
):
    if not user.role == "admin":
        raise HTTPException(
            status_code=403,
            detail="l'utilisateur doit être un administrateur.",
        )
    return user
