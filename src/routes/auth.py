from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from src.db.database import SessionDep
from src.models import Users
from src.utils.db_users import get_user_by_username
from src.utils.passwords import verify_hashed_password
from src.utils.auth import create_access_token

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login")
def login_user(session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()):
    invalid_cred_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid username or password"
    )
    db_user = get_user_by_username(form_data.username, session)
    if not db_user:
        raise invalid_cred_exception
    if not verify_hashed_password(form_data.password, db_user.password):
        raise invalid_cred_exception
    
    token = create_access_token({"id": db_user.id})
    return {"access_token": token, "token_type": "bearer"}
