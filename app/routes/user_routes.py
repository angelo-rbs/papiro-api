from math import log
from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.utils import get_value_or_default
from sqlalchemy.orm import Session

from app.db.models import UserModel
from app.depends import get_db_session

from app.schemas.auth_schema import LoginRequest
from app.schemas.user_schema import User, UserResponse
from app.use_cases.auth_user import UserUseCases

auth_router = APIRouter(prefix='/auth')

@auth_router.post('/registrar')
def registrar_usuario(
    user: User,
    db_session: Session = Depends(get_db_session)
):
    uc = UserUseCases(db_session)
    uc.user_register(user)

    return JSONResponse(
        content={'mensagem': 'Usuário criado com sucesso'},
        status_code=status.HTTP_201_CREATED
    )

@auth_router.post('/login')
def login(
    login_req: LoginRequest,
    db_session: Session = Depends(get_db_session)
):
    uc = UserUseCases(db_session)
    token = uc.user_login(login_req)

    return token


@auth_router.get('/', response_model=List[UserResponse])
def listar_usuarios(
    db_session: Session = Depends(get_db_session)
):
    uc = UserUseCases(db_session)
    users = uc.user_get_all()

    return users

@auth_router.delete('/delete-all')
def delete_all(
        db_session : Session = Depends(get_db_session)
):
    try:
        db_session.query(UserModel).delete()
        db_session.commit()
        return True
    except:
        db_session.rollback()
        return False


