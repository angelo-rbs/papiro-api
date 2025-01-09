from pydantic import field_validator, BaseModel, EmailStr
from datetime import datetime

class User(BaseModel):
    nome: str
    username: str
    email: EmailStr
    senha: str
    criadoEm: datetime
    ativo: bool

    @field_validator('username')
    def validate_username(cls, value):
        # TODO: validate username
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
