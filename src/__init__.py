from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.db.main import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server Starting.....")
    await init_db()
    yield
    print("Server Stopping.....")

app = FastAPI(
    title="Clubly",
    description="Information about footaball clubs",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {"message": "hello world!"}