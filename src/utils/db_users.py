from src.models import Users, UpdateUser
from fastapi import status, HTTPException, Depends
from sqlmodel import Session, select

from src.utils.passwords import hash_password

not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found"
)

def create_user(user_data: Users, session: Session):
    user_data.password = hash_password(user_data.password)
    session.add(user_data)
    session.commit()
    session.refresh(user_data)
    return user_data

def get_user(id: int, session: Session):
    db_user = session.get(Users, id)
    if not db_user:
        raise not_found_exception
    return db_user

def get_all_users(session: Session):
    stmt = select(Users)
    users = session.exec(stmt).all()
    return users

def get_user_by_username(username: str, session: Session):
    stmt = select(Users).where(Users.username == username)
    db_user = session.exec(stmt).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

def update_user(id: int, updated_data: UpdateUser, session:Session):
    db_user = session.get(Users, id)
    if not db_user:
        raise not_found_exception
    user = updated_data.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def delete_user(id: int, session: Session):
    db_user = session.get(Users, id)
    if not db_user:
        raise not_found_exception
    session.delete(db_user)
    session.commit()
    return {"ok": True}