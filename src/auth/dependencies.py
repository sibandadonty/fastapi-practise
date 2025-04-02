from fastapi.security import HTTPBearer
from fastapi import Depends, Request, HTTPException, status
from src.auth.auth import decode_token
from src.auth.redis import token_in_blocklist
from src.auth.schemas import UserModel
from src.auth.services import AuthService
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from typing import List
from src.errors import AccessTokenRequired, InvalidToken, RefreshTokenRequired

auth_services = AuthService()

class TokenBearer(HTTPBearer):

    def __init__(self, *, bearerFormat = None, scheme_name = None, description = None, auto_error = True):
        super().__init__(bearerFormat=bearerFormat, scheme_name=scheme_name, description=description, auto_error=auto_error)

    async def __call__(self, request: Request):
        creds = await super().__call__(request)

        token = creds.credentials
        
        token_data = decode_token(token)
        
        if await token_in_blocklist(token_data['jti']):
            raise InvalidToken()

        if not self.token_valid(token):
            raise InvalidToken()
        
        self.verify_token_data(token_data)

        return token_data
    
    def verify_token_data(self, token_data: dict):
       raise NotImplementedError("Method must be implemented in child classes")


    def token_valid(self, token: str):
        
        token_data = decode_token(token)

        return token_data is not None
    

class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict):
        if token_data and token_data["refresh"]:
            raise AccessTokenRequired()
        
class RefreshTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict):
        if token_data and not token_data["refresh"]:
            raise RefreshTokenRequired()
        
async def get_current_user(
        token_details: dict = Depends(AccessTokenBearer()),
        session: AsyncSession = Depends(get_session)):
    user_email = token_details["user"]["email"]
    
    user = await auth_services.get_user_by_email(user_email, session)

    return user

class RoleChecker:

    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: UserModel = Depends(get_current_user)):
        if current_user.roles in self.allowed_roles:
            return True
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not allowed to perform this operation"
        )
