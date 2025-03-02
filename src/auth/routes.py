from fastapi import Depends, HTTPException, status, APIRouter
from src.auth.schemas import UserCreateModel, UserModel
from src.db.main import get_session
from .services import AuthServices
from sqlalchemy.ext.asyncio.session import AsyncSession

auth_router = APIRouter()
auth_services = AuthServices()

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