from sqlmodel import Session, select
from src.models import Users, UpdateUser
from datetime import datetime, timezone
from fastapi import status, HTTPException
from src.utils.hash import hash_password

not_found_exp = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found"
)

def create_user(user_data: Users, session: Session):
    user_data.created_at = datetime.now(timezone.utc)
    user_data.password = hash_password(user_data.password)
    session.add(user_data)
    session.commit()
    session.refresh(user_data)
    return user_data

def get_user_by_email(email: str, session: Session):
    stmt = select(Users).where(Users.email == email)
    db_user = session.exec(stmt).first()
    print("db user from the source: ", db_user)
    if not db_user:
        raise not_found_exp
    return db_user

def get_all_users(session: Session):
    stmt = select(Users)
    db_users = session.exec(stmt).all()
    return db_users

def get_user(user_id: int, session: Session):
    db_user = session.get(Users, user_id)
    if not db_user:
        raise not_found_exp
    return db_user

def update_user(user_id: int, updated_data: UpdateUser, session: Session):
    db_user = session.get(Users, user_id)
    if not db_user:
        raise not_found_exp
    data = updated_data.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def delete_user(user_id: int, session: Session):
    db_user = session.get(Users, user_id)
    if not db_user:
        raise not_found_exp
    session.delete(db_user)
    session.commit()
    return {"ok": True}