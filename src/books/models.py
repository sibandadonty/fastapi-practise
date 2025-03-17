from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import date, datetime
import uuid

class Book(SQLModel, table=True):
    __tablename__ = "users"
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            index=True,
            nullable=False,
            unique=True,
            default=uuid.uuid4
        )
    )
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: date = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))