from fastapi import HTTPException, status, Depends
from jose import JWTError, jwt
from datetime import datetime, timezone, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from src.utils.db_users import get_user
from src.db.database import SessionDep

SECRET = "dcb46dee3838803b00b1c2fa22f49b13fd6ac723c3228e503d44f217e20e6429"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_TIME = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, expire_delta: timedelta | None = None):
    to_encode = data.copy()
    
    if expire_delta:
        expires = datetime.now(timezone.utc) + expire_delta 
    else:
        expires = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    to_encode.update({"exp": expires})
    encoded_jwt = jwt.encode(to_encode, SECRET, ALGORITHM)
    return encoded_jwt

def get_current_user(session: SessionDep, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        id: int = payload.get("id")
        if id is None: 
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    db_user = get_user(id, session)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user