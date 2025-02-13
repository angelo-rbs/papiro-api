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
