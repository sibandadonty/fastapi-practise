from fastapi import status, HTTPException
from src.models import TodoBase, Todo, TodoUpdate
from sqlmodel import Session, select

def create_todo(todo: Todo, session: Session):
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

def get_todo(id: int, session: Session):
    db_todo = session.get(Todo, id)
    if not db_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo Not Found")
    return db_todo

# def get_dotos(session: Session):
#     stmt = select(Todo)
#     todos = session.exec(stmt).all()
#     return todos

def get_todos(session: Session):
    stmt = select(Todo).offset(0).limit(30)
    todos = session.exec(stmt).all()
    return todos

def update_todo(id: int, todo_data: TodoUpdate, session: Session):
    db_todo = session.get(Todo, id)
    if not db_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo Not Found")
    todo = todo_data.model_dump(exclude_unset=True) 
    db_todo.sqlmodel_update(todo)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

def delete_todo(id: int, session: Session):
    db_todo = session.get(Todo, id)
    if not db_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo Not Found")
    session.delete(db_todo)
    session.commit()
    return {"ok": True}