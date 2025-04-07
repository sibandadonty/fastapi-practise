from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.db.main import init_db
from src.books.routes import book_router
from src.users.routes import users_router
from src.auth.routes import auth_router

version = "v1"

@asynccontextmanager
async def life_span(app: FastAPI):
    # await init_db()
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
app.include_router(users_router, prefix=f"/api/{version}/users", tags=["Users"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["Auth"])