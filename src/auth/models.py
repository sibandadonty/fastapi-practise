from sqlmodel import SQLModel, Field, Column
from datetime import datetime
import uuid
import sqlalchemy.dialects.postgresql as pg

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
    password: str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))