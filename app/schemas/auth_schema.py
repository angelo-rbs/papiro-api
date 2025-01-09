from enum import Enum
from pydantic import field_validator, BaseModel
from datetime import datetime

class TipoLogin(str, Enum):
    USERNAME = 'username'
    EMAIL = 'email'

class LoginRequest(BaseModel):
    credencial: str
    senha: str
    tipo_login: TipoLogin | None 

class TokenResponse(BaseModel):
    token_acesso: str
    expira_em: str
    tipo_token: str = 'Bearer'

