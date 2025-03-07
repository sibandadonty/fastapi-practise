from fastapi_mail import FastMail
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from .config import settings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

mail_conf = ConnectionConfig(
    MAIL_USERNAME = settings.MAIL_USERNAME,
    MAIL_PASSWORD = settings.MAIL_PASSWORD,
    MAIL_FROM = settings.MAIL_FROM,
    MAIL_PORT = settings.MAIL_PORT,
    MAIL_SERVER = settings.MAIL_SERVER,
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True,
    TEMPLATE_FOLDER=Path(BASE_DIR, "templates")
)

mail = FastMail(
    config=mail_conf
)

def create_message(recipients: str, subject: str, body: str):
    
    message = MessageSchema(
        recipients=recipients,
        subject=subject,
        body=body,
        subtype=MessageType.html
    )

    return message
