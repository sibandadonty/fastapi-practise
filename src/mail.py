from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from src.auth.schemas import EmailModel
from src.config import Config
from typing import List

conf = ConnectionConfig(
    MAIL_USERNAME = Config.MAIL_USERNAME,
    MAIL_PASSWORD = Config.MAIL_PASSWORD,
    MAIL_FROM = Config.MAIL_FROM,
    MAIL_PORT = Config.MAIL_PORT,
    MAIL_SERVER = Config.MAIL_SERVER,
    MAIL_STARTTLS = Config.MAIL_STARTTLS,
    MAIL_SSL_TLS = Config.MAIL_SSL_TLS,
    USE_CREDENTIALS = Config.USE_CREDENTIALS,
    VALIDATE_CERTS = Config.VALIDATE_CERTS
)

mail = FastMail(conf)

async def create_message(recipients: EmailModel, subject: str, body: str):
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=recipients,
        body=body,
        subtype=MessageType.html)
    
    return message
