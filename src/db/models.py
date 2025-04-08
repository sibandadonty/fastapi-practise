from typing import Optional, List
from sqlmodel import SQLModel, Field, Column, Relationship
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
    books: List["Book"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
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
    user: Optional[User] = Relationship(back_populates="books")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):
        return f"<Book {self.title}"