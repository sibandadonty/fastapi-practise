from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.responses import JSONResponse
from src.users.services import UserService
from src.db.main import get_session
from .schemas import UserLoginModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.auth.utils import verify_password
from src.auth.main import create_access_token
from src.auth.dependencies import AccessTokenBearer, RefreshTokenBearer, get_current_user
from src.auth.redis import add_token_to_blocklist
from src.users.schemas import UserModel

auth_router = APIRouter()
user_service = UserService()
access_token_bearer = AccessTokenBearer()
refresh_token_bearer = RefreshTokenBearer()

@auth_router.get("/me")
async def get_current_user(user: UserModel = Depends(get_current_user)):
    return user

@auth_router.post("/login")
async def login_user(login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password

    db_user = await user_service.get_user_by_email(email, session)

    if db_user:
        password_valid = verify_password(password, db_user.password)

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
                expiry=timedelta(days=2)
            )

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Login Successful",
                    "user_data": {
                    "email": db_user.email,
                    "uid": str(db_user.uid)
                    },
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }
            )
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid username or password"
    )

@auth_router.get("/renew_access_token")
async def renew_access_token(token_details: dict = Depends(refresh_token_bearer)):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_token = create_access_token(user_data=token_details["user"])

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "access_token": new_token
            }
        )
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Token is invalid or expired"
    )

@auth_router.get("/logout")
async def logout_user(token_details: dict = Depends(access_token_bearer)):

    jti = token_details["jti"]

    await add_token_to_blocklist(jti)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Logout successful"
        }
    )