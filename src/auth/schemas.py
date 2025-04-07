from sqlmodel import SQLModel

class UserLoginModel(SQLModel):
    email: str
    password: str

    