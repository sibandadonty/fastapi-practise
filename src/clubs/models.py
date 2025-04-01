from datetime import datetime
from typing import Optional
from  sqlmodel import Relationship, SQLModel, Field, Column
import uuid
import sqlalchemy.dialects.postgresql as pg

from src.auth.models import User

class Club(SQLModel, table=True):
    __tablename__ = "clubs"
    uid: uuid.UUID = Field(
        sa_column=Column(
          pg.UUID,
          primary_key=True,
          nullable=False,
          index=True,
          default=uuid.uuid4
        )
    )
    name: str
    location: str
    position: int
    ucl_trophies_number: int
    user: Optional[User] = Relationship(back_populates="clubs")
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))