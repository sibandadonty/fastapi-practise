from fastapi import FastAPI

app = FastAPI()

@app.get("/greet/{name}")
def root(name: str, age: int):
    return {"message": f"hello {name} you are {age} years old"}