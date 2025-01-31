from fastapi import APIRouter, Depends, status
from src.utils import db_users
from src.db.database import SessionDep
from src.models import Users, UpdateUser
from src.utils.auth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user_data: Users, session: SessionDep):
    return db_users.create_user(user_data, session)

@router.get("/")
def get_all_users(session: SessionDep, current_user: dict = Depends(get_current_user)):
    return db_users.get_all_users(session)

@router.get("/{id}")
def get_user(id: int, session: SessionDep, current_user: dict = Depends(get_current_user)):
    return db_users.get_user(id, session)

@router.patch("/{id}")
def update_user(id: int, updated_data: UpdateUser, session: SessionDep, current_user: dict = Depends(get_current_user)):
    return db_users.update_user(id, updated_data, session)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, session: SessionDep, current_user: dict = Depends(get_current_user)):
    return db_users.delete_user(id, session)