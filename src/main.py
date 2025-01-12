from  fastapi import FastAPI
from src.routes import todos
from src.db.database import create_db_and_tables

app = FastAPI()

app.include_router(todos.router)

@app.on_event("startup")
def startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "hello  world"}