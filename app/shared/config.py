from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(env_path)


class Config(BaseSettings):
    APP_ENV: str
    LOG_LEVEL: str

    DATABASE_URL: str
    DB_HOST: str
    DB_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    MOCK_DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=env_path, env_file_encoding="utf-8", extra="ignore")


config = Config()
