from typing import List
from sqlmodel import Column, Relationship, SQLModel, Field
import uuid
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg
from src.books import models

class User(SQLModel, table=True):
    __tablename__ = "users"
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            nullable=False,
            default=uuid.uuid4
        )
    )
    email: str
    username: str
    role: str = Field(
        sa_column=Column(
            pg.VARCHAR,
            nullable=False,
            server_default="user"
        )
    )
    first_name: str
    last_name: str
    password: str = Field(exclude=True)
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    books: List["models.Books"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})