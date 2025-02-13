from fastapi import Request
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError, field_validator, BaseModel, EmailStr
from datetime import datetime

from app.exceptions import (
    NotFoundException,
    PapiroApiException,
)


class User(BaseModel):
    nome: str
    username: str
    email: EmailStr
    senha: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        # raise PapiroApiException("nao encontrado mano")
        raise ValueError()
        return value


class UserRequest(User):
    pass


class UserResponse(BaseModel):
    id: int
    nome: str
    username: str
    email: EmailStr
    criadoEm: datetime
    ativo: bool
