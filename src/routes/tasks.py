from fastapi import APIRouter, status
from src.models import Task, UpdateTask
from src.db.database import SessionDep
from src.utils import db_tasks

router = APIRouter(prefix="/tasks")

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_task(task: Task, session: SessionDep):
    return db_tasks.create_task(task, session)

@router.get("/")
def get_all_tasks(session: SessionDep):
    return db_tasks.get_tasks(session)

@router.get("/{id}")
def get_task(id: int, session: SessionDep):
    return db_tasks.get_task(id, session)

@router.patch("/{id}")
def update_tasks(id: int, update_data: UpdateTask, session:SessionDep):
    return db_tasks.update_task(id, update_data, session)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int, session: SessionDep):
    return db_tasks.delete_task(id, session)
