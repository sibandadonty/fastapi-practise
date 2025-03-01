from fastapi import FastAPI, Header
from typing import Optional
from contextlib import asynccontextmanager
from src.db.main import init_db

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

@app.get("/greet/{name}")
def root(name: Optional[str] = "User", age: int = 0):
    return {"message": f"hello {name} you are {age} years old"}

@app.get("/get_headers")
def get_headers(
    host: str = Header(None),
    accept: str = Header(None),
    content_type: str = Header(None)
    ):
    request_header = {}
    request_header["Host"] = host
    request_header["Accept"] = accept
    request_header["Content-Type"] = content_type
    return request_header