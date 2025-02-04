from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime

class Task(SQLModel, table=True):
    id: int | None = Field(None, primary_key=True, index=True)
    title: str
    description: str
    isDone: bool

class UpdateTask(SQLModel):
    title: str | None = None
    description: str | None = None
    isDone: bool | None = None
    

class Users(SQLModel, table=True):
    id: int | None = Field(None, primary_key=True, index=True)
    username: str = Field(..., unique=True, index=True)
    password: str
    created_at: Optional[datetime] = None

class UpdateUser(SQLModel):
    username: str | None = None