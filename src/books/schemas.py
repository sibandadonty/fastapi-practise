from datetime import datetime, date
import uuid
from pydantic import BaseModel

class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    published_date: date
    publisher: str
    page_count: int
    language: str
    created_at: datetime 
    updated_at: datetime 

    # class Config:
    #     from_attributes = True

class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str

class BookCreateModel(BookUpdateModel):
    published_date: str