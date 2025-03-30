from fastapi import APIRouter, status, HTTPException
from .services import ClubService
from .models import Club
from .schemas import ClubModel, UpdateClubModel, CreateClubModel

club_router = APIRouter()
club_service = ClubService()

# @club_router.get("/")
# def get_all_clubs(session: )