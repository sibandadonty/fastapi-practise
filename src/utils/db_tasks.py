from fastapi import status, HTTPException
from src.db.database import SessionDep
from src.models import Task, UpdateTask
from sqlmodel import select

not_found_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

def create_task(data: Task, session: SessionDep):
    session.add(data)
    session.commit()
    session.refresh(data)
    return data

def get_task(id: int, session: SessionDep):
    task = session.get(Task, id)
    if not task:
        raise not_found_exception
    return task

def get_tasks(session: SessionDep):
    stmt = select(Task)
    tasks = session.exec(stmt).all()
    return tasks

def update_task(id: int, update_data: UpdateTask, session: SessionDep):
    db_task = session.get(Task, id)
    if not db_task:
        raise not_found_exception
    task = update_data.model_dump(exclude_unset=True)
    db_task.sqlmodel_update(task)
    session.add(db_task)
    session.commit()
    session.refresh()
    return db_task

def delete_task(id: int, session: SessionDep):
    db_task = session.get(Task, id)
    if not db_task:
        raise not_found_exception
    session.delete(db_task)
    return {"ok": True}