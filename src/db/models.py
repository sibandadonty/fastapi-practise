from typing import Optional
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import date, datetime
import uuid

class User(SQLModel, table=True):
    __tablename__ = "users"
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            unique=True,
            index=True,
            default=uuid.uuid4,
            primary_key=True
        )
    )
    username: str
    email: str
    role: str = Field(sa_column=Column(pg.VARCHAR, server_default="user", nullable=False))
    password: str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):
        return f"<User {self.email}>"
    
class Book(SQLModel, table=True):
    __tablename__ = "books"
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            unique=True,
            primary_key=True,
            index=True,
            default=uuid.uuid4
        )
    )
    title: str
    description: str
    author: str
    published_date: date
    user_uid: Optional[uuid.UUID] = Field(None, foreign_key="users.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):
        return f"<Book {self.title}"