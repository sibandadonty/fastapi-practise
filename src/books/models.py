from datetime import datetime, date
from typing import Optional
from sqlmodel import Column, Relationship, SQLModel, Field
import sqlalchemy.dialects.postgresql as pg
import uuid
from src.auth import models

class Books(SQLModel, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            nullable=False,
            default=uuid.uuid4
        )
    )
    title: str
    author: str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    published_date: date
    publisher: str
    page_count: int
    language: str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    user: Optional["models.User"] = Relationship(back_populates="books")