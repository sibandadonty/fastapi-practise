from typing import Optional
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timezone, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from src.utils.db_users import get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

ACCESS_TOKEN_EXPIRE_TIME = 30
ALGORITHM = "HS256"
SECRET_KEY = "9330aae4dee5f637a931a78adb9e98bf9c346ee91452906d99a781f2b00940fa"

def create_access_token(data: dict, expire_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
    else: 
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(session: Session, token: str = Depends(oauth2_scheme)):
    unathorized_exp = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        if not payload:
            raise unathorized_exp
    except JWTError:
        raise unathorized_exp
    
    db_user = get_user_by_email(payload.email, session)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return db_user

    
    


    
