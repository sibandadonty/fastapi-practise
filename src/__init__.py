from fastapi import FastAPI

version = "v1"

app = FastAPI(
    title="Bookly",
    description="Backend for an app to read and review books",
    version=version
)

@app.get("/")
async def root():
    return {"message": "hello  world"}