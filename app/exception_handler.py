import types
from typing import MutableSequence
from fastapi import status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from starlette.types import ExceptionHandler
from pydantic import ValidationError


from app.exceptions import (
    AlreadyExistsException,
    InvalidEntityException,
    InvalidOperationException,
    InvalidTokenException,
    NotFoundException,
    PapiroApiException,
    UnauthorizedException,
)


def criar_exception_handler(
    status_code: int, descricao_inicial: str
) -> ExceptionHandler:
    response = {"mensagem": descricao_inicial}

    async def exception_handler(_: Request, ex: Exception) -> JSONResponse:
        if isinstance(ex, RequestValidationError):
            mensagem = "[Validation]: Erro de validação"
            content = {
                "mensagem": mensagem,
                "detalhes": None,
            }

            if ex.errors():
                obj = ex.errors()[0]
                mensagem = f"[Validation] {format_pydantinc_error_message(obj['msg'])}"

                content = jsonable_encoder(
                    {
                        "mensagem": mensagem,
                        "detalhes": ex.errors()[0],
                    }
                )

            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content=content,
            )

        elif isinstance(ex, PapiroApiException):
            if ex.message:
                response["mensagem"] = ex.message

            if ex.name:
                response["mensagem"] = f"[{ex.name}] {response['mensagem']}"

            return JSONResponse(
                status_code=status_code, content={"mensagem": response["mensagem"]}
            )

        else:
            return JSONResponse(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detalhes": "Internal server error"},
            )

    return exception_handler


def attach_exception_handlers(app):
    app.add_exception_handler(
        exc_class_or_status_code=RequestValidationError,
        handler=criar_exception_handler(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "RequestValidationError capturado"
        ),
    )

    app.add_exception_handler(
        exc_class_or_status_code=PapiroApiException,
        handler=criar_exception_handler(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Serviço indisponível"
        ),
    )

    app.add_exception_handler(
        exc_class_or_status_code=NotFoundException,
        handler=criar_exception_handler(
            status.HTTP_404_NOT_FOUND, "Objeto não encontrado"
        ),
    )

    app.add_exception_handler(
        exc_class_or_status_code=UnauthorizedException,
        handler=criar_exception_handler(
            status.HTTP_401_UNAUTHORIZED, "Autorização negada"
        ),
    )

    app.add_exception_handler(
        exc_class_or_status_code=AlreadyExistsException,
        handler=criar_exception_handler(
            status.HTTP_400_BAD_REQUEST, "Conflito: entidade já existente"
        ),
    )

    app.add_exception_handler(
        exc_class_or_status_code=InvalidTokenException,
        handler=criar_exception_handler(status.HTTP_401_UNAUTHORIZED, "Token inválido"),
    )

    app.add_exception_handler(
        exc_class_or_status_code=InvalidOperationException,
        handler=criar_exception_handler(
            status.HTTP_400_BAD_REQUEST, "Operação inválida"
        ),
    )

    app.add_exception_handler(
        exc_class_or_status_code=InvalidEntityException,
        handler=criar_exception_handler(
            status.HTTP_400_BAD_REQUEST, "Entidade inválida"
        ),
    )


def format_pydantinc_error_message(msg: str):
    if msg.startswith("Value error, "):
        if msg == "Value error, ":
            return "Erro de validação"
        else:
            return msg[13:]
    else:
        return msg
