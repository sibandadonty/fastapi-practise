from datetime import timedelta, datetime
from fastapi import Depends, HTTPException, status, APIRouter
from src.auth.schemas import EmailModel, UserBooksModel, UserCreateModel, UserModel, UserLoginModel
from src.db.main import get_session
from src.errors import UserNotFound
from .services import AuthServices
from sqlalchemy.ext.asyncio.session import AsyncSession
from .utils import create_access_token
from .utils import verify_password
from src.config import settings
from fastapi.responses import JSONResponse
from .dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user, RoleChecker
from src.db.redis import add_jti_to_blocklist
from src.mail import mail, create_message
from .utils import hash_password, create_url_safe_token, decode_url_safe_token

auth_router = APIRouter()
auth_services = AuthServices()
role_checker = RoleChecker(["admin", "user"])

@auth_router.post("/send_mail")
async def send_mail(emails: EmailModel):
    message = create_message(
        recipients=emails.addresses,
        subject="welcome",
        body="<h1>Welcome to the app<h1>"
    )
     
    await mail.send_message(message)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="email sent successfully"
    )


@auth_router.get("/verify/{token}")
async def verify_email(token: str, session: AsyncSession = Depends(get_session)):
    token_data = decode_url_safe_token(token)
    user_email = token_data.get("email")

    if user_email:
        user = await auth_services.get_user_by_email(user_email, session)

        if not user:
            raise UserNotFound()
            
        await auth_services.update_user({"is_verified": True}, user, session)

        return JSONResponse(
            content={"message": "Account verified successfully"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "Error occured during verification"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    user_exist = await auth_services.user_exist(user_data.email, session)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with email already exist"
        )
    user = await auth_services.create_user(user_data, session)
    token = create_url_safe_token({"email": user_data.email})

    link = f"http://{settings.DOMAIN}/api/v1/users/verify/{token}"

    html_message = f"""
    <h1>Verify your email</h1>
    <p>Click this <a href={link}>link</a> to verify</p>
    """
    
    message = create_message(
        recipients=[user_data.email],
        subject="Verify your email",
        body=html_message
    )
     
    await mail.send_message(message)

    return {
        "message": "Account created successfully! now open you email and verify your account",
        "user": user
    }

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

@auth_router.get("/me", response_model=UserBooksModel)
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