from sqlmodel import SQLModel
from datetime import datetime, date
import uuid

class BookCreateModel(SQLModel):
    title: str
    description: str
    author: str
    published_date: str

class BookUpdateModel(SQLModel):
    title: str | None = None
    description: str | None = None
    author: str | None = None
    published_date: str | None = None

class BookModel(BookCreateModel):
    uid: uuid.UUID
    created_at: datetime 
    published_date: date
