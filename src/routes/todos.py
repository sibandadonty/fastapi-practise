from fastapi import APIRouter
from src.utils import db_todos
from src.db.database import SessionDep
from src.models import Todo, TodoBase, TodoUpdate

router = APIRouter(
    tags=["Todos"],
    prefix="/todos"
)

@router.post("/")
def create_todo(todo: Todo, session: SessionDep):
    return db_todos.create_todo(todo, session)

@router.get("/")
def get_todos(session: SessionDep):
    return db_todos.get_todos(session)

@router.get("/{id}")
def get_todos(id: int, session: SessionDep):
    return db_todos.get_todo(id, session)

@router.patch("/{id}")
def update_todo(id: int, todo_data: TodoUpdate, session: SessionDep):
    return db_todos.update_todo(id, todo_data, session)

@router.delete("/{id}")
def get_todos(id: int, session: SessionDep):
    return db_todos.delete_todo(id, session)