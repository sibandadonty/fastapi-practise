from fastapi import FastAPI
from src.db.database import create_db_and_tables
from src.routes import tasks, users, auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
"http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.on_event("startup")
def startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "Hello World"}