from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException, status, Depends
from src.auth.main import decode_token
from src.auth.redis import token_in_blocklist
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.users.schemas import UserModel
from src.users.services import UserService
from typing import List
from src.errors import AccessTokenRequired, RefreshTokenRequired

user_service = UserService()

class TokenBearer(HTTPBearer):
    def __init__(self, *, bearerFormat = None, scheme_name = None, description = None, auto_error = True):
        super().__init__(bearerFormat=bearerFormat, scheme_name=scheme_name, description=description, auto_error=auto_error)

    async def __call__(self, request: Request):
        creds = await super().__call__(request)

        token = creds.credentials
        token_details = decode_token(token)
        
        if await token_in_blocklist(token_details["jti"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token is invalid or revoked"
            )

        if not self.token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token is invalid or expired"
            )
         
        self.verify_token_details(token_details)

        return token_details
    
    def token_valid(self, token: str):

        token_details = decode_token(token)

        return token_details is not None
    
    def verify_token_details(self, token_details: dict):
        raise NotImplementedError("This method must be implemented in child classes")
    

class AccessTokenBearer(TokenBearer):
    def verify_token_details(self, token_details):
        if token_details and token_details["refresh"]:
            raise AccessTokenRequired()
        
class RefreshTokenBearer(TokenBearer):
    def verify_token_details(self, token_details):
        if token_details and not token_details["refresh"]:
            raise RefreshTokenRequired()
        

async def get_current_user(session: AsyncSession = Depends(get_session), token_details: dict = Depends(AccessTokenBearer())):
    email = token_details["user"]["email"]

    user = await user_service.get_user_by_email(email, session)

    return user

class RoleChecker:
    def __init__(self, allowed_list: List[str]):
        self.allowed_list = allowed_list

    def __call__(self, current_user: UserModel = Depends(get_current_user)):
        if current_user.role in self.allowed_list:
            return True
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not allowed to perform this operation"
        )