from datetime import datetime, date
from typing import List, Optional
import uuid
from pydantic import BaseModel
from src.reviews.schemas import Review 
from src.auth.schemas import UserModel

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

class BookDetailsModel(Book):
    uid: uuid.UUID
    rating: int
    review_text: str
    user_uid: uuid.UUID 
    book_uid: uuid.UUID 
    created_at: datetime 
    updated_at: datetime 
    user: UserModel
    book: Book 
   

class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str

class BookCreateModel(BookUpdateModel):
    published_date: str