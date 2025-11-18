from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(env_path)


class Config(BaseSettings):
    APP_ENV: str
    LOG_LEVEL: str

    DATABASE_URL: Optional[str] = None
    DB_HOST: Optional[str] = None
    DB_PORT: Optional[int] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    MOCK_DATABASE_URL: Optional[str] = None

    model_config = SettingsConfigDict(env_file=env_path, env_file_encoding="utf-8", extra="ignore")

    @model_validator(mode="after")
    def validate_database_config(self):
        if self.APP_ENV == "test":
            if not self.MOCK_DATABASE_URL:
                raise ValueError("MOCK_DATABASE_URL is required when APP_ENV=test")
        else:
            if not self.DATABASE_URL:
                raise ValueError("DATABASE_URL is required when APP_ENV is not 'test'")
            if not self.DB_HOST:
                raise ValueError("DB_HOST is required when APP_ENV is not 'test'")
            if self.DB_PORT is None:
                raise ValueError("DB_PORT is required when APP_ENV is not 'test'")
            if not self.POSTGRES_USER:
                raise ValueError("POSTGRES_USER is required when APP_ENV is not 'test'")
            if not self.POSTGRES_PASSWORD:
                raise ValueError("POSTGRES_PASSWORD is required when APP_ENV is not 'test'")
            if not self.POSTGRES_DB:
                raise ValueError("POSTGRES_DB is required when APP_ENV is not 'test'")
        return self


config = Config()
