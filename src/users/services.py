from sqlmodel import select
from fastapi import HTTPException, status
from src.db.models import User
from .schemas import UserCreateModel, UserUpdateModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.auth.utils import hash_password

class UserService:

    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        results = await session.execute(statement)
        user = results.scalar()
        return user if user is not None else None
    
    async def user_exist(self, email: str, session: AsyncSession):
        user = await self.get_user_by_email(email, session)
        return True if user is not None else False
    
    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        
        user_data_dict = user_data.model_dump()

        new_user = User(**user_data_dict)

        new_user.password = hash_password(new_user.password)

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user