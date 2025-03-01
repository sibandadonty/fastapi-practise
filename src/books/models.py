from datetime import datetime
from sqlmodel import Column, SQLModel, Field
import sqlalchemy.dialects.postgresql as pg
import uuid

class Books(SQLModel, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            nullable=False,
            default=uuid.uuid4()
        )
    )
    title: str
    author: str
    published_date: str
    publisher: str
    page_count: int
    language: str
    created_at: datetime = Field(Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(Column(pg.TIMESTAMP, default=datetime.now))
    