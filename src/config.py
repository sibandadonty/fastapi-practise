from pydantic_settings import BaseSettings, SettingsConfigDict
from os import path

env_path = path.join(path.dirname(__file__), ".env")

class Settings(BaseSettings):
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=env_path,
        extra="ignore"
    )

Config = Settings()