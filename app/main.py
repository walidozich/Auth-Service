from fastapi import FastAPI
from app.api.v1.auth import router as auth_router
from app.models.user import Base
from app.core.database import engine

app = FastAPI(title="FastAPI JWT Auth Service")

app.include_router(auth_router, prefix="/api/v1")
