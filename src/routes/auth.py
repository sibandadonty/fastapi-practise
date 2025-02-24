from src.utils import db_users
from src.db.database import SessionDep
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.auth import oauth2_scheme, create_access_token
from src.utils.db_users import get_user_by_email
from src.utils.hash import verify_password

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login")
def login(session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = get_user_by_email(form_data.username, session)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password"
        )
    
    if verify_password(form_data.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password"
        )
     
    access_token = create_access_token({"email": db_user.email})
    return {"access_toekn": access_token, "token_type": "Bearer"}
