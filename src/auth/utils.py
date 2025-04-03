import logging
from passlib.context import CryptContext
from itsdangerous import URLSafeTimedSerializer
from src.config import Config

password_ctx = CryptContext(
    schemes=["bcrypt"]
)

serializer = URLSafeTimedSerializer(
    secret_key=Config.JWT_SECRET,
    salt="email-configaration"
)

def hash_password(password: str):
    return password_ctx.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return password_ctx.verify(plain_password, hashed_password)

def create_url_safe_token(data: dict):
    token = serializer.dumps(data)
    return token

def decode_url_safe_token(token: str):
    try:
        token_data = serializer.loads(token)
        return token_data
    except Exception as e:
        logging.exception(e)