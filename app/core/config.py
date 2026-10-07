import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "Food Lens Nutrition Engine"
    API_V1_STR: str = "/api/v1"
    
    # Environment & Security
    ENV: str = "development"
    SECRET_KEY: str = "super_secret_dev_key_change_in_production_12345"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days
    
    # External API Keys
    GEMINI_API_KEY: str
    
    # Database Settings
    # Set USE_SQLITE=True for instant local testing, or False when PostgreSQL service is running
    USE_SQLITE: bool = True
    
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "food_analyzer_db"
    
    DATABASE_URL: Optional[str] = None
    ASYNC_DATABASE_URL: Optional[str] = None

    # Firebase Storage Configuration
    FIREBASE_CREDENTIALS_PATH: Optional[str] = None
    FIREBASE_STORAGE_BUCKET: Optional[str] = None
    UPLOAD_DIR: str = str(ROOT_DIR / "uploads")

    model_config = SettingsConfigDict(
        env_file=str(ROOT_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def get_async_db_url(self) -> str:
        if self.USE_SQLITE:
            db_path = str(ROOT_DIR / "food_analyzer.db")
            return f"sqlite+aiosqlite:///{db_path}"
        if self.ASYNC_DATABASE_URL:
            return self.ASYNC_DATABASE_URL
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    def get_sync_db_url(self) -> str:
        if self.USE_SQLITE:
            db_path = str(ROOT_DIR / "food_analyzer.db")
            return f"sqlite:///{db_path}"
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Settings()
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
