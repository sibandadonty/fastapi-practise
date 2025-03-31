from sqlmodel import SQLModel
import uuid
from datetime import datetime

class CreateUserModel(SQLModel):
    username: str
    email: str
    password: str

class UpdateUserModel(SQLModel):
    pass

class UserModel(CreateUserModel):
    uid: uuid.UUID
    created_at: datetime