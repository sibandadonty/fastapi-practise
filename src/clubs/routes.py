from fastapi import APIRouter, status, HTTPException, Depends
from .services import ClubService
from .models import Club
from .schemas import ClubModel, UpdateClubModel, CreateClubModel
from src.db.main import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import List
from src.auth.dependencies import AccessTokenBearer, RoleChecker

club_router = APIRouter()
club_service = ClubService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["admin", "user"]))

not_found_exp = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Club not found"
)

@club_router.get("/", response_model=List[ClubModel], dependencies=[role_checker])
async def get_all_clubs(session: AsyncSession = Depends(get_session), token_details: dict = Depends(access_token_bearer)):
    print(token_details)
    return await club_service.get_all_clubs(session)

@club_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Club, dependencies=[role_checker])
async def create_club(club_data: CreateClubModel, token_details: dict = Depends(access_token_bearer), session: AsyncSession = Depends(get_session)):
    user_uid = token_details["user"]["uid"]
    return await club_service.create_club(club_data, user_uid ,session)

@club_router.get("/{club_uid}", response_model=Club, dependencies=[role_checker])
async def get_club(club_uid: str, session: AsyncSession = Depends(get_session)):
    db_club = await club_service.get_club(club_uid, session) 

    if db_club is None:
        raise not_found_exp
    
    return db_club

@club_router.patch("/{club_uid}", response_model=Club, dependencies=[role_checker])
async def update_club(club_uid: str, club_update_data: UpdateClubModel, session: AsyncSession = Depends(get_session)):
    db_club = await club_service.update_club(club_uid, club_update_data, session)

    if db_club is None:
        raise not_found_exp
    
    return db_club

@club_router.delete("/{club_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker])
async def delete_club(club_uid: str, session: AsyncSession = Depends(get_session)):
    db_club = await club_service.delete_club(club_uid, session)

    if db_club is None:
        raise not_found_exp
    
    return {}

