from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logger import logger
from app.db.session import engine
from app.db.base import Base
from app.api.v1.api import api_router

# Import models here to ensure they are registered with Base.metadata
from app.models.user import User
from app.models.task import Task

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        description="REST API for PrimeTrade Intern Assignment (Refactored)",
        version="1.1.0"
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    def on_startup():
        logger.info("Initializing PrimeTrade API...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables verified.")

    @app.get("/health", tags=["System"])
    def health_check():
        return {"status": "ok", "app": settings.PROJECT_NAME}

    # Include API Router
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app

app = create_app()
