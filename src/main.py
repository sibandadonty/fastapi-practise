from fastapi import FastAPI
from src.db.database import create_db_and_tables
from src.routes import users

app = FastAPI()

app.include_router(users.router)

@app.on_event("startup")
def startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "Hello World!!!"}