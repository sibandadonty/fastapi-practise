from fastapi import APIRouter, status, HTTPException, Depends
from .services import UserService
from .schemas import UserCreateModel, UserUpdateModel, UserModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.db.main import get_session

users_router = APIRouter()
users_service = UserService()

not_found_exp = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found"
)

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

@users_router.get("/")
async def get_all_user(session: AsyncSession = Depends(get_session)):
    users = await users_service.get_all_user(session)
    return users

@users_router.get("/{user_uid}")
async def get_user(user_uid: str, session: AsyncSession = Depends(get_session)):
    user = await users_service.get_user(user_uid, session)
    
    if not user:
        raise not_found_exp
    
    return user

@users_router.patch("/{user_uid}")
async def update_user(user_uid: str, update_data: UserUpdateModel, session: AsyncSession = Depends(get_session)):
    updated_user = await users_service.update_user(user_uid, update_data, session)

    if not updated_user:
        raise not_found_exp
    
    return updated_user

@users_router.delete("/{user_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_uid: str, session: AsyncSession = Depends(get_session)):
    results = await users_service.delete_user(user_uid, session)

    if results is None:
        raise not_found_exp
    
    return {}