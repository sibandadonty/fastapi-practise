from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.db.main import init_db
from src.books.routes import book_router
version = "v1"

@asynccontextmanager
async def life_span(app: FastAPI):
    await init_db()
    print("server started....")
    yield
    print("server stopped....")

app = FastAPI(
    title="Bookly",
    description="Backend for an app to read and review books",
    version=version,
    lifespan=life_span
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["Books"])
