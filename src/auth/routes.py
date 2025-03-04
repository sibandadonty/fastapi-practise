from datetime import timedelta, datetime
from fastapi import Depends, HTTPException, status, APIRouter
from src.auth.schemas import UserCreateModel, UserModel, UserLoginModel
from src.db.main import get_session
from .services import AuthServices
from sqlalchemy.ext.asyncio.session import AsyncSession
from .utils import create_access_token
from .utils import verify_password
from src.config import settings
from fastapi.responses import JSONResponse
from .dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user, RoleChecker
from src.db.redis import add_jti_to_blocklist


auth_router = APIRouter()
auth_services = AuthServices()
role_checker = RoleChecker(["admin", "user"])

@auth_router.post("/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    user_exist = await auth_services.user_exist(user_data.email, session)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with email already exist"
        )
    user = await auth_services.create_user(user_data, session)
    return user

@auth_router.post("/login")
async def login_user(user_login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    email = user_login_data.email
    password = user_login_data.password
    
    user = await auth_services.get_user_by_email(email, session)
    
    if user is not None:
        valid_password = verify_password(password, user.password)
        if valid_password:
            access_token = create_access_token(
                user_data={
                    "email": user.email,
                    "uid": str(user.uid)
                }
            )

            refresh_token = create_access_token(
                user_data={
                    "email": user.email,
                    "uid": str(user.uid)
                },
                expiry=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_TIME),
                refresh=True
            )

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "email": user.email,
                        "uid": str(user.uid)
                    }
                }
            )
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid Email or Password"
    )

@auth_router.get("/refresh_token")
async def create_new_access_token(user_details = Depends(RefreshTokenBearer())):
    expiry_timestamp = user_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_token = create_access_token(
            user_data=user_details["user"]
        )
        return {
            "access_token": new_token
        }
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Token is invalid or expired"
    )

@auth_router.get("/me")
async def get_current_user(user = Depends(get_current_user), _ = Depends(role_checker)):
    return user

@auth_router.get("/logout")
async def logout_user(user_details = Depends(AccessTokenBearer())):
    jti = user_details["jti"]

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={
            "message": "Logged out sucessfully"
        }
    )