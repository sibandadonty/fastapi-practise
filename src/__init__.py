from fastapi import FastAPI, Header
from typing import Optional
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.books.routes import book_router
from src.auth.routes import auth_router

@asynccontextmanager
async def life_span(app: FastAPI):
    print("server getting started....")
    await init_db()
    yield
    print("server is stopping....")

version = "v1"
app = FastAPI(
    version=version,
    title="Bookly",
    description="AN API for books",
    lifespan=life_span
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["Books"])
app.include_router(auth_router, prefix=f"/api/{version}/users", tags=["Auth"])