from pydantic_settings import BaseSettings, SettingsConfigDict
from os import path

env_path = path.join(path.dirname(__file__), ".env")

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRY_TIME: int

    model_config = SettingsConfigDict(
        env_file=env_path,
        extra="ignore"
    )

Config = Settings()