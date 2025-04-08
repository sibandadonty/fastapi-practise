from typing import List
from sqlmodel import SQLModel
from datetime import datetime
from src.books.schemas import BookModel
import uuid

class UserCreateModel(SQLModel):
    username: str
    email: str
    password: str

class UserModel(UserCreateModel):
    uid: uuid.UUID
    role: str
    created_at: datetime 

class UserBookModel(UserModel):
    books: List[BookModel]

class UserUpdateModel(SQLModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None