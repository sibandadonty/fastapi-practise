import uuid
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from src.config import settings
import jwt
import logging
from itsdangerous import URLSafeTimedSerializer

password_ctx = CryptContext(schemes=["bcrypt"])

def hash_password(password: str):
    return password_ctx.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return password_ctx.verify(plain_password, hashed_password)

def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False):
    payload = {}

    payload["user"] = user_data
    payload["exp"] = datetime.now() + (expiry if expiry is not None else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_TIME))
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh

    access_token = jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    return access_token

def verify_token(token: str):
    try:
        payload = jwt.decode(
            jwt=token,
            algorithms=[settings.JWT_ALGORITHM],
            key=settings.JWT_SECRET
        )
        return payload
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
    

serializer = URLSafeTimedSerializer(
    secret_key=settings.JWT_SECRET,
    salt="email-configuration"
)

def create_url_safe_token(data: dict):

    token = serializer.dumps(data)

    return token

def decode_url_safe_token(token: str):
    try:
        token_data = serializer.loads(token)
        return token_data
    except Exception as e:
        logging.error(str(e))
