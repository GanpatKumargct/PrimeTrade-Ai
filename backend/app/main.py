from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.logger import logger
from app.database import engine, Base
from app import auth, tasks

# Import all models here so that Base.metadata.create_all can find them
# This is a temporary measure until Alembic is introduced (if needed)

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        description="REST API for PrimeTrade Intern Assignment",
        version="1.0.0"
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # In production, restrict this to frontend domain
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    def on_startup():
        logger.info("Initializing PrimeTrade API...")
        # Create database metadata
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables verified.")

    @app.get("/health", tags=["System"])
    def health_check():
        return {"status": "ok", "app": settings.PROJECT_NAME}

    app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Auth"])
    app.include_router(tasks.router, prefix=f"{settings.API_V1_STR}/tasks", tags=["Tasks"])

    return app

app = create_app()
