from sqlmodel import SQLModel
import uuid
from datetime import datetime

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
    role: str