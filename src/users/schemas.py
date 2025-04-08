from sqlmodel import SQLModel
from datetime import datetime
import uuid

class UserCreateModel(SQLModel):
    username: str
    email: str
    password: str

class UserModel(UserCreateModel):
    uid: uuid.UUID
    role: str
    created_at: datetime 

class UserUpdateModel(SQLModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None