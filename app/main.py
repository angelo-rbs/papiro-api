from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.exception_handler import attach_exception_handlers
from app.routes.user_routes import auth_router

from fastapi.exceptions import RequestValidationError

app = FastAPI()

attach_exception_handlers(app)
app.include_router(auth_router)


@app.get("/")
def health_check():
    return "server running"


# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(
#     _: Request, ex: RequestValidationError
# ) -> JSONResponse:
#     """Handler global para capturar erros de validação do Pydantic"""
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content={"mensagem": "Erro de validação", "detalhes": ex.errors()},
#     )
