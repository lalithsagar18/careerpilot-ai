import os
from typing import List, Optional, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore",
        case_sensitive=True
    )

    ENVIRONMENT: str = "development"
    PROJECT_NAME: str = "CareerPilot AI"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "insecure-dev-secret-key-change-in-production-min32chars"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    ALGORITHM: str = "HS256"

    # Server & CORS
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    FRONTEND_URL: str = "http://localhost:3000"
    BACKEND_URL: str = "http://localhost:8000"
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]

    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "careerpilot_user"
    POSTGRES_PASSWORD: str = "careerpilot_secret"
    POSTGRES_DB: str = "careerpilot_db"
    
    # SQLite fallback for local test/dev when Postgres isn't running
    DATABASE_URL: Optional[str] = None
    SYNC_DATABASE_URL: Optional[str] = None

    # AI Configuration
    LLM_PROVIDER: str = "gemini"  # "gemini", "openai", "mock"
    LLM_API_KEY: Optional[str] = None
    LLM_MODEL: str = "gemini-1.5-pro"
    EMBEDDING_PROVIDER: str = "gemini"  # "gemini", "mock"
    EMBEDDING_MODEL: str = "models/text-embedding-004"
    EMBEDDING_DIMENSION: int = 768

    # Oracle Compatibility Flag
    ORACLE_ENABLED: bool = False
    ORACLE_USER: Optional[str] = None
    ORACLE_PASSWORD: Optional[str] = None
    ORACLE_DSN: Optional[str] = None

    # Security & Limits
    MAX_UPLOAD_SIZE_BYTES: int = 10 * 1024 * 1024  # 10 MB
    ALLOWED_UPLOAD_EXTENSIONS: List[str] = ["pdf", "docx", "txt", "md"]
    RATE_LIMIT_PER_MINUTE: int = 60

    def get_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    def get_sync_database_url(self) -> str:
        if self.SYNC_DATABASE_URL:
            return self.SYNC_DATABASE_URL
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Settings()
