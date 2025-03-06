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
    create_exception_handler
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

def register_error_handlers(app: FastAPI):
    app.add_exception_handler(
        BookNotFound, 
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "book not found",
                "error_code": "book_not_found"
            }
        ))
    
    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Please provide a valid access token",
                "resolution": "Please get an access token",
                "error_code": "access_token_required",
            },
        ),
    )

    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Please provide a valid refresh token",
                "resolution": "Please get an refresh token",
                "error_code": "refresh_token_required",
            },
        ),
    )

@app.exception_handler(500)
def internal_server_error(request, exe):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content="Ooop something went wrong with the server"
    )

register_error_handlers(app)
app.include_router(book_router, prefix=f"/api/{version}/books", tags=["Books"])
app.include_router(auth_router, prefix=f"/api/{version}/users", tags=["Auth"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["Reviews"])