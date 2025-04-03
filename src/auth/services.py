from sqlalchemy.ext.asyncio.session import AsyncSession
from src.auth.schemas import CreateUserModel, UpdateUserModel
from src.auth.models import User
from src.auth.utils import hash_password
from sqlmodel import select
from fastapi import HTTPException, status

class AuthService:
    
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        user = result.scalar()
        return user
    
    async def user_exist(self, email: str, session: AsyncSession):
        user = await self.get_user_by_email(email, session)
        return True if user is not None else False

    async def create_user(self, user_data:CreateUserModel, session: AsyncSession):
        
        user_exist = await self.user_exist(user_data.email, session)
        if user_exist == True:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exist"
            )

        user_data_dict = user_data.model_dump()
        new_user = User(**user_data_dict)
        new_user.password = hash_password(new_user.password)
        # new_user.club_uid = club_uid

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
    
    async def get_user(self, user_uid: str, session: AsyncSession):
        statement = select(User).where(User.uid == user_uid)
        results = await session.execute(statement)
        user = results.scalar()
        return user

    
    async def update_user(self,user_uid: str, update_data: UpdateUserModel, session: AsyncSession):
        db_user = await self.get_user(user_uid, session)
        
        if db_user:
            user_data_dict = update_data.model_dump(exclude_unset=True)

            for k,v in user_data_dict.items():
                setattr(db_user, k, v)

            await session.commit()
            await session.refresh(db_user)
            return db_user
        else:
            return None
        