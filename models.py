from sqlmodel import SQLModel, Field, DateTime
from datetime import datetime

class Todo(SQLModel, table=True):
    id: int | None = Field(default=None, index=True, primary_key=True)
    title: str
    description: str
    created_at: DateTime = Field(default=datetime.utcnow())