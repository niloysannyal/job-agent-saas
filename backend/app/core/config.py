from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

# Base repository root directory (for resolving relative file paths across environments)
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
CANONICAL_DB_FILE = (REPO_ROOT / "backend" / "job_agent.db").as_posix()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Job Application Agent SaaS"
    API_V1_PREFIX: str = "/api/v1"

    # Adzuna API credentials
    ADZUNA_APP_ID: Optional[str] = None
    ADZUNA_APP_KEY: Optional[str] = None
    ADZUNA_BASE_URL: str = "https://api.adzuna.com/v1/api"

    # Database (defaults to canonical SQLite in backend directory, overridden by DATABASE_URL in .env)
    DATABASE_URL: Optional[str] = f"sqlite:///{CANONICAL_DB_FILE}"


    # OpenAI & LLM Settings
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"

    # Vector Database
    QDRANT_URL: str = "http://localhost:6333"

    # Authentication & JWT Configuration
    JWT_SECRET_KEY: str = "jobeazy-saas-super-secret-jwt-key-phase0-2026"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Google OAuth 2.0 Credentials (for Gmail Draft composition)
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GOOGLE_REDIRECT_URI: str = "http://localhost:5173/auth/google/callback"

    # Redis URL (for background async worker Arq)
    REDIS_URL: str = "redis://localhost:6379/0"

    # Profile & CV Template Paths (configurable via environment variables)
    MASTER_CV_PATH: Path = Path("cv_templates/01_MASTER_CV.tex")
    USER_PROFILE_PATH: Path = Path("docs/USER_PROFILE.md")

    def resolve_cv_path(self) -> Path:
        """Resolve the Master CV path from explicit, local, or repository root paths."""
        if self.MASTER_CV_PATH.is_absolute() and self.MASTER_CV_PATH.exists():
            return self.MASTER_CV_PATH
        if self.MASTER_CV_PATH.exists():
            return self.MASTER_CV_PATH.resolve()
        candidate = REPO_ROOT / self.MASTER_CV_PATH
        return candidate if candidate.exists() else self.MASTER_CV_PATH

    def resolve_profile_path(self) -> Path:
        """Resolve the User Profile path from explicit, local, or repository root paths."""
        if self.USER_PROFILE_PATH.is_absolute() and self.USER_PROFILE_PATH.exists():
            return self.USER_PROFILE_PATH
        if self.USER_PROFILE_PATH.exists():
            return self.USER_PROFILE_PATH.resolve()
        candidate = REPO_ROOT / self.USER_PROFILE_PATH
        return candidate if candidate.exists() else self.USER_PROFILE_PATH

    model_config = SettingsConfigDict(
        env_file=(str(REPO_ROOT / "backend" / ".env"), ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )



settings = Settings()
