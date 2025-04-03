import logging
from fastapi import HTTPException, status
from passlib.context import CryptContext
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from src.config import Config

password_ctx = CryptContext(
    schemes=["bcrypt"]
)

salt = "email-configaration"

serializer = URLSafeTimedSerializer(
    secret_key=Config.JWT_SECRET,
    salt=salt
)

def hash_password(password: str):
    return password_ctx.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return password_ctx.verify(plain_password, hashed_password)

def create_url_safe_token(data: dict, expires_in=3600):
    token = serializer.dumps(data, salt=salt)
    return token

def decode_url_safe_token(token: str, max_age=3600):
    try:
        token_data = serializer.loads(token, salt=salt, max_age=max_age)
        return token_data
    except SignatureExpired as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token is expired")
    except BadSignature as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token is invalid")
        