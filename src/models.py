from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Users(SQLModel, table=True):
    id: Optional[int] = Field(None, primary_key=True)
    name: str
    email: str
    password: str
    created_at: datetime

class UpdateUser(SQLModel):
    email: str
    name: str
    