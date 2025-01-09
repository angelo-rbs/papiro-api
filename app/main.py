from fastapi import FastAPI

from app.routes.user_routes import auth_router
app = FastAPI()

app.include_router(auth_router)

@app.get("/")
def health_check():
    return "server running"

