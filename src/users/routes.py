from fastapi import APIRouter, status, HTTPException, Depends
from .services import UserService
from .schemas import UserCreateModel, UserUpdateModel, UserModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.db.main import get_session

users_router = APIRouter()
users_service = UserService()

@users_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    user_exist = await users_service.user_exist(user_data.email, session)

    if not users_service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email address already exist"
        )
    
    new_user = await users_service.create_user(user_data, session)

    return new_user