from fastapi import APIRouter, Depends
from .services import AuthService
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.auth.schemas import CreateUserModel, UpdateUserModel, UserModel
from src.auth.models import User
from src.db.main import get_session

auth_router = APIRouter()
auth_service = AuthService()

@auth_router.post("/signup", response_model=UserModel)
async def create_user(user_data: CreateUserModel, session: AsyncSession = Depends(get_session)):
    user = await auth_service.create_user(user_data, session)
    return user