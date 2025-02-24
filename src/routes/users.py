from src.utils import db_users
from src.db.database import SessionDep
from fastapi import APIRouter, status
from src.models import Users, UpdateUser

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/")
def create_user(user_data: Users, session: SessionDep):
    return db_users.create_user(user_data, session)

@router.get("/")
def get_all_users(session: SessionDep):
    return db_users.get_all_users(session)

@router.get("/{id}")
def get_user(id: int, session: SessionDep):
    return db_users.get_user(id, session)

@router.patch("/{id}", status_code=status.HTTP_201_CREATED)
def update_user(id: int, updated_data: UpdateUser, session: SessionDep):
    return db_users.update_user(id, updated_data, session)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, session: SessionDep):
    return db_users.delete_user(id, session)