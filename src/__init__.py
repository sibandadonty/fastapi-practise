from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.db.main import init_db
from src.clubs.routes import club_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server Starting.....")
    await init_db()
    yield
    print("Server Stopping.....")

version = "v1"

app = FastAPI(
    title="Clubly",
    description="Information about footaball clubs",
    version=version,
    lifespan=lifespan
)

app.include_router(club_router, prefix=f"/api/{version}/clubs", tags=["Clubs"])
