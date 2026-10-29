from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.admin import router as admin_router
from app.api.applications import router as applications_router
from app.api.auth import router as auth_router
from app.api.interview import router as interview_router
from app.api.integrations import router as integrations_router
from app.api.jobs import router as jobs_router
from app.api.profile import router as profile_router
from app.db.base import Base
from app.db.seed import seed_initial_data
from app.db.session import get_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure database tables exist on startup
    Base.metadata.create_all(bind=get_engine())
    seed_initial_data()
    yield


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
        lifespan=lifespan,
    )

    # Enable CORS for frontend clients
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health", tags=["health"])
    def health_check():
        return {"status": "ok"}

    # Register API v1 prefix routes
    app.include_router(auth_router, prefix=settings.API_V1_PREFIX)
    app.include_router(jobs_router, prefix=settings.API_V1_PREFIX)
    app.include_router(applications_router, prefix=settings.API_V1_PREFIX)
    app.include_router(profile_router, prefix=settings.API_V1_PREFIX)
    app.include_router(interview_router, prefix=settings.API_V1_PREFIX)
    app.include_router(integrations_router, prefix=settings.API_V1_PREFIX)
    app.include_router(admin_router, prefix=settings.API_V1_PREFIX)

    return app



app = create_app()
