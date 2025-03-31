from fastapi import APIRouter, Depends, status, HTTPException
from .services import AuthService
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.auth.schemas import CreateUserModel, UpdateUserModel, UserModel, LoginModel
from src.auth.models import User
from src.db.main import get_session
from src.auth.utils import verify_password
from src.auth.auth import create_access_token
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from src.auth.dependencies import RefreshTokenBearer, AccessTokenBearer

auth_router = APIRouter()
auth_service = AuthService()
refresh_token_bearer = RefreshTokenBearer()
access_token_bearer = AccessTokenBearer()

@auth_router.post("/login")
async def login_user(login_data: LoginModel, session: AsyncSession = Depends(get_session)):
    db_user = await auth_service.get_user_by_email(login_data.email, session)

    if db_user is not None:
        password_valid = verify_password(login_data.password, db_user.password)

        if password_valid:
            access_token = create_access_token(
                user_data={
                    "email": db_user.email,
                    "uid": str(db_user.uid)
                },
            )

            refresh_token = create_access_token(
                user_data={
                    "email": db_user.email,
                    "uid": str(db_user.uid)
                },
                refresh=True,
                expiry=timedelta(minutes=1440)
            )

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "access_token": access_token,
                    "token_type": "Bearer",
                    "refresh_token": refresh_token,
                    "user_data": {
                    "email": db_user.email,
                    "uid": str(db_user.uid)
                },
              }
            )
        
    raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password"
        )

@auth_router.post("/signup", response_model=UserModel)
async def create_user(user_data: CreateUserModel, session: AsyncSession = Depends(get_session)):
    user = await auth_service.create_user(user_data, session)
    return user

@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(refresh_token_bearer)):
    expiry_timestamp = token_details['exp']

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(token_details['user'])

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"access_token": new_access_token}
        )
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid or expired token"
    )