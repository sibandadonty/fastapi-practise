from pydantic_settings import BaseSettings, SettingsConfigDict
import os

env_path = os.path.join(os.path.dirname(__file__), ".env")

class Settings(BaseSettings):
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=env_path,
        extra="ignore"
    )

Config = Settings()

