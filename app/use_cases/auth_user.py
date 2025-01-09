from datetime import date, datetime, timedelta, timezone
from hashlib import algorithms_available
from math import log
from os import access

from decouple import config
from fastapi import status
from fastapi.exceptions import HTTPException
from jose import jwt, JWTError
from jose.constants import ALGORITHMS
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.db.models import UserModel
from app.schemas.auth_schema import LoginRequest, TokenResponse
from app.schemas.user_schema import User

crypto_context = CryptContext(schemes=['sha256_crypt'])
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

class UserUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def user_register(self, user: User):
        user_model = UserModel(
            nome=user.nome,
            username=user.username,
            email=user.email,
            senha=crypto_context.hash(user.senha),
            criadoEm=user.criadoEm,
            ativo=user.ativo
        )
        try:
            self.db_session.add(user_model)
            self.db_session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Usuário já existe'
            )

    def user_login(self, login_req: LoginRequest, expires_in_minutes: int = 30):

        # busca por username
        user_on_db = (
            self.db_session.query(UserModel)
            .filter((UserModel.username == login_req.credencial) | (UserModel.email == login_req.credencial))
            .first()
        )

        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Nome de usuário ou senha inválidos'
            )


        if not crypto_context.verify(login_req.senha, user_on_db.senha):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Nome de usuário ou senha inválidos'
            )

        return self.__criar_token_acesso(user_on_db, expires_in_minutes)

    def __criar_token_acesso(self, user: UserModel, duration_in_minutes: int):
        exp = datetime.now(timezone.utc) + timedelta(minutes=duration_in_minutes)

        payload = {
            'sub': user.username,
            'exp': exp.isoformat()
        }

        access_token = jwt.encode(payload, key=SECRET_KEY, algorithm=ALGORITHM)

        return TokenResponse(
            token_acesso=access_token,
            expira_em=exp.isoformat(), 
            tipo_token='Bearer'
        ) 

    def user_get_all(self):
        return self.db_session.query(UserModel).all()

    