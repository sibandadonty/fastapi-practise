from fastapi import status, HTTPException
from src.models import Task, UpdateTask
from sqlmodel import select, Session

not_found_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

def create_task(data: Task, session: Session):
    session.add(data)
    session.commit()
    session.refresh(data)
    return data

def get_task(id: int, session: Session):
    task = session.get(Task, id)
    if not task:
        raise not_found_exception
    return task

def get_tasks(session: Session):
    stmt = select(Task)
    tasks = session.exec(stmt).all()
    return tasks

def update_task(id: int, update_data: UpdateTask, session: Session):
    db_task = session.get(Task, id)
    if not db_task:
        raise not_found_exception
    task = update_data.model_dump(exclude_unset=True)
    db_task.sqlmodel_update(task)
    session.add(db_task)
    session.commit()
    session.refresh()
    return db_task

def delete_task(id: int, session: Session):
    db_task = session.get(Task, id)
    if not db_task:
        raise not_found_exception
    session.delete(db_task)
    return {"ok": True}