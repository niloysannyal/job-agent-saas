from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Job Application Agent SaaS"
    API_V1_PREFIX: str = "/api/v1"

    # Adzuna API credentials
    ADZUNA_APP_ID: Optional[str] = None
    ADZUNA_APP_KEY: Optional[str] = None
    ADZUNA_BASE_URL: str = "https://api.adzuna.com/v1/api"

    # Database
    DATABASE_URL: Optional[str] = "postgresql+psycopg2://postgres:postgres@localhost:5432/job_agent"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
