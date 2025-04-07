from datetime import timedelta
from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.responses import JSONResponse
from src.users.services import UserService
from src.db.main import get_session
from .schemas import UserLoginModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.auth.utils import verify_password
from src.auth.main import create_access_token

auth_router = APIRouter()
user_service = UserService()

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
       