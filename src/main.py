from fastapi import FastAPI, Header
from typing import Optional

app = FastAPI()

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