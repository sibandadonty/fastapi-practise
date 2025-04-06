from datetime import datetime, timedelta
import logging
import jwt
import uuid
from src.config import Config
from typing import Optional

def create_access_token(user_data: dict, expiry: Optional[timedelta] = None, refresh: Optional[bool] = False):
    payload = {
        "user": user_data,
        "exp": datetime.now() + (expiry if expiry is not None else timedelta(minutes=Config.ACCESS_TOKEN_EXPIRY_TIME)),
        "jti": str(uuid.uuid4()),
        "refresh": refresh
    }

    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET_KEY,
        algorithm=Config.JWT_ALGORITHM
    )

    return token

def decode_token(token: str):
    try:
        token_data = jwt.decode(
          jwt=token,
          algorithms=[Config.JWT_ALGORITHM],
          key=Config.JWT_SECRET_KEY
        )

        return token_data
    except jwt.PyJWTError as pjwte: 
        logging.exception(pjwte)
        return None
    except Exception as e:
        logging.exception(e)
        return None
   
   