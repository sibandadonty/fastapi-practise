from fastapi import FastAPI
from src.books.routes import book_router
from src.db.main import initdb
from contextlib import asynccontextmanager

version="v1"

@asynccontextmanager
async def lifespan(app: FastAPI):
    await initdb()
    print("server started.......")
    yield
    print("server stopped.......")

app = FastAPI(
    title="Bookly",
    description="A simple API for managing books",
    version=version,
    lifespan=lifespan
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])