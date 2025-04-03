from typing import List
from sqlmodel import SQLModel
import uuid
from datetime import datetime

from src.clubs.schemas import ClubModel

class LoginModel(SQLModel):
    email: str
    password: str

class CreateUserModel(SQLModel):
    username: str
    email: str
    password: str

class UpdateUserModel(SQLModel):
    pass

class UserModel(SQLModel):
    uid: uuid.UUID
    created_at: datetime
    username: str
    email: str
    roles: str

class UpdateUserModel(SQLModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
    is_verified: bool | None = None
    
class UserBooksModel(UserModel):
    clubs: List[ClubModel]

class EmailModel(SQLModel):
    addresses: List[str]

class PasswordResetRequest(SQLModel):
    email: str

class PasswordResetConfirm(SQLModel):
    old_password: str
    new_password: str
