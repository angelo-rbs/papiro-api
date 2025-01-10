from fastapi import FastAPI, Request

from fastapi import status
from fastapi.responses import JSONResponse
from starlette.types import ExceptionHandler

from app.routes.user_routes import auth_router
from app.exceptions import AlreadyExistsException, InvalidOperationException, InvalidTokenException, NotFoundException, PapiroApiException, UnauthorizedException

app = FastAPI()

app.include_router(auth_router)

@app.get("/")
def health_check():
    return "server running"


def criar_exception_handler(
    status_code:int, descricao_inicial: str
) -> ExceptionHandler:
    detalhes = {"mensagem": descricao_inicial}

    async def exception_handler(_: Request, ex: PapiroApiException) -> JSONResponse:
        if ex.message:
            detalhes["mensagem"] = ex.message

        if ex.name:
            detalhes["mensagem"] = f"{detalhes['mensagem']} [{ex.name}]"

        return JSONResponse(
            status_code=status_code, content={"detalhes": detalhes["mensagem"]}
        )

    return exception_handler

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
    handler=criar_exception_handler(
        status.HTTP_401_UNAUTHORIZED, "Token inválido"
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=InvalidOperationException,
    handler=criar_exception_handler(
        status.HTTP_400_BAD_REQUEST, "Operação inválida"
    ),
)
