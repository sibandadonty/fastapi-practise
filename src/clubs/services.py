from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from .schemas import CreateClubModel, UpdateClubModel
from .models import Club

class ClubService:

    async def get_user_clubs(self, user_uid: str, session: AsyncSession):
        statement = select(Club).where(Club.user_uid == user_uid).order_by(desc(Club.created_at))

        results = await session.execute(statement)

        clubs = results.scalars().all()

        return clubs

    async def create_club(self, club_data: CreateClubModel, user_uid: str, session: AsyncSession):
        club_data_dict = club_data.model_dump()
        new_club = Club(**club_data_dict)
        new_club.user_uid = user_uid
        session.add(new_club)
        await session.commit()
        await session.refresh(new_club)
        
        return new_club
    
    async def get_club(self, club_uid: str, session: AsyncSession):
        statement = select(Club).where(Club.uid == club_uid)
        result = await session.execute(statement)
        club = result.scalar()
        return club if club is not None else None
    
    async def get_all_clubs(self, session: AsyncSession):
        statement = select(Club)
        result = await session.execute(statement)
        clubs = result.scalars().all()
        return clubs
    
    async def update_club(self, club_uid: str, club_update_data: UpdateClubModel, session: AsyncSession):
        club_to_update = await self.get_club(club_uid, session)

        if club_to_update is not None:
            club_update_data_dict = club_update_data.model_dump()

            for k,v in club_update_data_dict.items():
                setattr(club_to_update, k, v)

            await session.commit()

            return club_to_update
        else:
            return None

    async def delete_club(self, club_uid: str, session: AsyncSession):
        club_to_delete = await self.get_club(club_uid, session)

        if club_to_delete:
            await session.delete(club_to_delete)
            await session.commit()
            return {}
        else:
            return None   
