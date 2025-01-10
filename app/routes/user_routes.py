from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.models import UserModel
from app.depends import get_db_session

from app.schemas.user_schema import User, UserResponse
from app.use_cases.auth_user import UserUseCases

auth_router = APIRouter(prefix='/auth')


@auth_router.post('/registrar', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(
    user: User,
    db_session: Session = Depends(get_db_session)
):
    'Registra um novo usuário'
    uc = UserUseCases(db_session)
    user_criado = uc.user_register(user)

    return user_criado

@auth_router.post('/login')
def login(
    login_form: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_db_session)
):
    'Verifica credenciais e retorna token de acesso'
    uc = UserUseCases(db_session)
    token = uc.user_login(login_form)

    return token


@auth_router.get('/', response_model=List[UserResponse])
def listar_usuarios(
    db_session: Session = Depends(get_db_session)
):
    'Lista todos os usuários'
    uc = UserUseCases(db_session)
    users = uc.user_get_all()

    return users

@auth_router.delete('/delete-all')
def delete_all(
        db_session : Session = Depends(get_db_session)
):
    'Remove todos os usuários'
    try:
        db_session.query(UserModel).delete()
        db_session.commit()
        return True
    except:
        db_session.rollback()
        return False


