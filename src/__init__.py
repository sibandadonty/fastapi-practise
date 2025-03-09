from fastapi import FastAPI, Header, status
from typing import Optional
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from src.db.main import init_db
from src.books.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from src.errors import (
    register_error_handlers,
    register_middleware
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
    redoc_url=f"/api/{version}/redoc",
    docs_url=f"/api/{version}/docs",
    contact={
        "email": "sibandadonty@gmail.com",
        "phone_number": "039249220424"
    },
    lifespan=life_span
)

register_error_handlers(app)
register_middleware(app)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["Books"])
app.include_router(auth_router, prefix=f"/api/{version}/users", tags=["Auth"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["Reviews"])