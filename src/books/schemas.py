from datetime import datetime, date
from pydantic import BaseModel

class Book(BaseModel):
    uid: str
    title: str
    author: str
    published_date: date
    publisher: str
    page_count: int
    language: str
    created_at: datetime 
    updated_at: datetime 

class BookCreateModel(BaseModel):
    title: str
    author: str
    published_date: str
    publisher: str
    page_count: int
    language: str

class BookUpdateModel(BookCreateModel):
    pass