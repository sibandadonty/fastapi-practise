from sqlmodel import select
from src.db.models import User
from src.auth.schemas import UserCreateModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from .utils import hash_password

class AuthServices:
    
    async def get_user_by_email(self, email:str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        user = result.scalar()
        return user
    
    async def user_exist(self, email: str, session: AsyncSession):
        user = await self.get_user_by_email(email, session)

        return True if user is not None else False
    
    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()
        
        new_user = User(
            **user_data_dict
        )
        new_user.password = hash_password(user_data_dict["password"])
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)        
        return new_user
    
    # async def update_user(self,update_data: dict, user: User, session: AsyncSession):

    #     for k,v in update_data.items():
    #         setattr(user.model_dump(), k, v)

    #     await session.commit()
    #     await session.refresh(user)
    #     return user
    
    async def update_user(self, user:User , user_data: dict,session:AsyncSession):

        for k, v in user_data.items():
            setattr(user, k, v)

        await session.commit()

        return user
