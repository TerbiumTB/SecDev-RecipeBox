# import os
# from dataclasses import dataclass

# from dotenv import load_dotenv

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    DATABASE_URL: str
    MOCK_DATABASE_URL: str
    APP_ENV: str
    LOG_LEVEL: str
    # def validate(self):
    #     missing = [k for k, v in vars(self).items() if v is None]
    #     if missing:
    #         raise RuntimeError(f"Missing required secrets: {missing}")

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env", env_file_encoding="utf-8"
    )


# load_dotenv()
config = Config()
