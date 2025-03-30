import jwt
from src.config import Config
from datetime import datetime, timedelta
from typing import Optional
import uuid
import logging

TOKEN_EXPIRY_TIME = 30

def create_access_token(user_data: dict, expiry: Optional[timedelta] = None, refresh: bool = False):
    token = jwt.encode(
        payload={
           "user": user_data,
           "jti": str(uuid.uuid4()),
           "exp": (datetime.now() + expiry if expiry is not None else timedelta(minutes=TOKEN_EXPIRY_TIME)),
           "refresh": refresh 
        },
        algorithm=Config.JWT_ALGORITHM,
        key=Config.JWT_SECRET
    )

    return token

def decode_token(token: str):
    try:
        payload = jwt.decode(
           jwt=token,
           algorithms=[Config.JWT_ALGORITHM],
           key=Config.JWT_SECRET
        )
        return payload
    except jwt.PyJWKError as e:
        logging.exception(e)
        return None
    except Exception as e:
        logging.exception(e)
        return None
    