from fastapi import FastAPI, Header, status
from typing import Optional
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from src.db.main import init_db
from src.books.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from src.errors import (
    BookNotFound,
    RefreshTokenRequired,
    AccessTokenRequired,
    create_exception_handler,
    register_error_handlers
)

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



register_error_handlers(app)
app.include_router(book_router, prefix=f"/api/{version}/books", tags=["Books"])
app.include_router(auth_router, prefix=f"/api/{version}/users", tags=["Auth"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["Reviews"])