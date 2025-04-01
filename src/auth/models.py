from typing import Optional, List
from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
# from src.clubs.models import Club
import uuid

class User(SQLModel, table=True):
    __tablename__ = "users"
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            unique=True,
            nullable=False,
            default=uuid.uuid4
        )
    )
    username: str
    email: str
    roles: str = Field(sa_column=Column(pg.VARCHAR, server_default="user"))
    clubs: List["Club"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    password: str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))