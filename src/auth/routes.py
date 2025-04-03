from fastapi import APIRouter, Depends, status, HTTPException

from src.config import Config
from src.errors import InvalidEmailOrPassword
from .services import AuthService
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.auth.schemas import CreateUserModel, EmailModel, UpdateUserModel, UserModel, LoginModel, UserBooksModel
from src.auth.models import User
from src.db.main import get_session
from src.auth.utils import verify_password
from src.auth.auth import create_access_token
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from src.auth.dependencies import RefreshTokenBearer, AccessTokenBearer, RoleChecker, get_current_user
from src.auth.redis import add_token_to_blocklist
from src.mail import mail, create_message
from src.auth.utils import create_url_safe_token

auth_router = APIRouter()
auth_service = AuthService()
refresh_token_bearer = RefreshTokenBearer()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["admin", "user"]))


@auth_router.post("/send_mail")
async def send_mail(receipents: EmailModel):
    body = "<h1>Welcome to my app clubly</h1>"
    addresses = receipents.addresses

    message = create_message(
        recipients=addresses,
        subject="Welcome to Clubly",
        body=body
    )

    await mail.send_message(message)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Email sent successfully"
    )

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
        
    raise InvalidEmailOrPassword()

@auth_router.post("/signup")
async def create_user(user_data: CreateUserModel, session: AsyncSession = Depends(get_session)):
    user = await auth_service.create_user(user_data, session)
    
    email = user.email
    
    token = create_url_safe_token({"email": email})

    link = f"http://{Config.DOMAIN}/api/v1/verify/{token}"

    html_message = f"""
    <h1>Verify your email</h1>
    <p>Click on this <a href={link}>link</a> to verify your email</p>
    """

    message = create_message(
        recipients=[email],
        subject="Verify your email",
        body=html_message
    )

    await mail.send_message(message)

    return {
        "message": "Account created successfully check you email for an email to verify your account",
        "user": user
    }

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

@auth_router.get("/logout")
async def logut_user(token_details: dict = Depends(access_token_bearer)):

    jti = token_details['jti']

    await add_token_to_blocklist(jti)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Logged out successfully"
    )

@auth_router.get("/me", dependencies=[role_checker], response_model=UserBooksModel)
async def get_current_loggedin_user(user: UserModel =Depends(get_current_user)):
    return user