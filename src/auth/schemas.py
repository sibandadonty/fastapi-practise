from datetime import datetime
from typing import List
import uuid
from pydantic import BaseModel, Field
from src.db.models import Books

class UserModel(BaseModel):
    uid: uuid.UUID
    email: str
    username: str
    first_name: str
    last_name: str
    password: str = Field(exclude=True)
    is_verified: bool 
    created_at: datetime 
    updated_at: datetime 
    books: List[Books]

class UserCreateModel(BaseModel):
    email: str
    first_name: str
    last_name: str
    username: str
    password: str

class UserLoginModel(BaseModel):
    email: str
    password: str