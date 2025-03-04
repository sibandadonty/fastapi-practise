from typing import List
from fastapi.security import HTTPBearer
from src.auth.utils import verify_token
from fastapi import Depends, status, HTTPException, Request
from src.db.redis import token_in_blocklist
from src.db.main import get_session
from src.auth.services import AuthServices
from sqlalchemy.ext.asyncio.session import AsyncSession

auth_services = AuthServices()

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request):
        creds = await super().__call__(request)
        
        token = creds.credentials
        
        token_data = verify_token(token)
        
        if not await self.token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "Token is expired or invalid",
                    "resolution": "Get a new token"
                }
            )
        
        if await token_in_blocklist(token_data["jti"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "Token is invalid or has been revoked",
                    "resolution": "Get a new token"
                }
            )

        self.verify_token_data(token_data)

        return token_data
    
    def verify_token_data(self, token_data: dict):
        raise NotImplementedError("Implement this method in child classes")

    async def token_valid(self, token: str):
        token = verify_token(token)

        return token is not None
    
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict):
        if token_data and token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token"
            )
        
class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict):
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a refresh token"
            )

async def get_current_user(token_details=  Depends(AccessTokenBearer()), session: AsyncSession = Depends(get_session)):
    email = token_details["user"]["email"]

    user = await auth_services.get_user_by_email(email, session)

    return user

class RoleChecker:

    def __init__(self, allowed_roles: List["str"]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user = Depends(get_current_user)):
        
        if current_user.role in self.allowed_roles:
            return True
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not permited to perform this operation"
        )
        