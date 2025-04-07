from sqlmodel import select
from fastapi import HTTPException, status
from src.db.models import User
from .schemas import UserCreateModel, UserUpdateModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.auth.utils import hash_password

not_found_exp = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found"
)

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
    
    async def get_all_user(self, session: AsyncSession):
        statement = select(User)
        results = await session.execute(statement)
        users = results.scalars().all()
        return users
    
    async def get_user(self, user_uid: str, session: AsyncSession):
        statement = select(User).where(User.uid == user_uid)
        results = await session.execute(statement)
        user = results.scalar()
        return user
    
    async def update_user(self, user_uid: str, update_data: UserUpdateModel, session: AsyncSession):
        db_user = await self.get_user(user_uid, session)

        if db_user is not None:
            update_data_dict = update_data.model_dump(exclude_unset=True)

            for k, v in update_data_dict.items():
                setattr(db_user ,k, v)
            
            await session.commit()
            await session.refresh(db_user)
            return db_user
        
        else:
            return None
            
    async def delete_user(self, user_uid: str, session: AsyncSession):
        db_user = await self.get_user(user_uid, session)

        if db_user is not None:
            await session.delete(db_user)
            await session.commit()
            return {}
        else: 
            return None
        
