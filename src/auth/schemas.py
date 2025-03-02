from datetime import datetime
import uuid
from pydantic import BaseModel, Field

class UserModel(BaseModel):
    uid: uuid.UUID
    email: str
    username: str
    first_name: str
    last_name: str
    password: str = Field(exclude=True)
    is_verified: bool 
    created_at: datetime 
    updated_at: datetime 

class UserCreateModel(BaseModel):
    email: str
    first_name: str
    last_name: str
    username: str
    password: str