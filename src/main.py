from fastapi import FastAPI

app = FastAPI()

@app.get("/greet/{name}")
def root(name: str):
    return {"message": f"hello {name}"}