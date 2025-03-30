from sqlmodel import SQLModel
import uuid
from datetime import datetime

class Club(SQLModel):
    uid: uuid.UUID
    name: str
    location: str
    position: int
    ucl_trophies_number: int
    created_at: datetime

class CreateClubModel(SQLModel):
    name: str
    location: str
    position: int
    ucl_trophies_number: int

class UpdateClubModel(CreateClubModel):
    pass