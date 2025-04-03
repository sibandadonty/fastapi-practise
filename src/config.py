from pydantic_settings import BaseSettings, SettingsConfigDict
from os import path

env_path = path.join(path.dirname(__file__), ".env")

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    MAIL_PASSWORD: str
    MAIL_USERNAME: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_STARTTLS: bool = False,
    MAIL_SSL_TLS: bool = True,
    USE_CREDENTIALS: bool = True,
    VALIDATE_CERTS: bool = True

    model_config = SettingsConfigDict(
        env_file=env_path,
        extra="ignore"
    )

Config = Settings()