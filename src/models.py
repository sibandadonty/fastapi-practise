from sqlmodel import SQLModel, Field, DateTime
from datetime import datetime

class TodoBase(SQLModel):
    title: str
    description: str

class TodoUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    isComplete: bool | None = None

class Todo(TodoBase, table=True):
    id: int | None = Field(default=None, index=True, primary_key=True)
    isComplete: bool = Field(default=False)
    created_at: str = Field(default="2025-01-12T12:56:28.560427")