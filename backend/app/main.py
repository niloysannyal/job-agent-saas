from fastapi import FastAPI
from app.core.config import settings
from app.api.jobs import router as jobs_router


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    )

    @app.get("/health", tags=["health"])
    def health_check():
        return {"status": "ok"}

    # Register API v1 prefix routes
    app.include_router(jobs_router, prefix=settings.API_V1_PREFIX)

    return app


app = create_app()
