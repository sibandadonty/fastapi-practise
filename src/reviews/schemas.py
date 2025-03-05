from datetime import datetime
import uuid
from pydantic import BaseModel
from sqlalchemy.dialects import postgresql as pg
from sqlmodel import Field, Column

class Review(BaseModel):
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            nullable=False,
            default=uuid.uuid4
        )
    )
    rating: int
    review_text: str
    user_uid: uuid.UUID 
    book_uid: uuid.UUID 
    created_at: datetime 
    updated_at: datetime 

class CreateReviewModel(BaseModel):
    rating: int
    review_text: str