import json
from typing import Annotated, Optional
from pydantic import AfterValidator, BaseModel, Field


def validate_user_role(role: str):
    if not role in ["user", "admin"]:
        raise ValueError(f"Le role doit être user ou admin")
    return role


class UserResponseSchema(BaseModel):
    id: int
    email: str
    password: str
    role: str


class UserCreateSchema(BaseModel):
    email: str
    password: Annotated[str, Field(min_length=2)]
    role: Optional[Annotated[str, AfterValidator(validate_user_role)]] = "user"


class UserUpdateSchema(BaseModel):
    password: Optional[Annotated[str, Field(min_length=2)]] = None
    role: Optional[Annotated[str, AfterValidator(validate_user_role)]] = None


class UserLoginSchema(BaseModel):
    email: str
    password: Annotated[str, Field(min_length=2)]


class UserLoggedInSchema(BaseModel):
    email: str
    role: str
