from fastapi.security import HTTPBearer
from fastapi import Depends, Request, HTTPException, status
from src.auth.auth import decode_token
from src.auth.redis import token_in_blocklist
from src.auth.services import AuthService
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.db.main import get_session

auth_services = AuthService()

class TokenBearer(HTTPBearer):

    def __init__(self, *, bearerFormat = None, scheme_name = None, description = None, auto_error = True):
        super().__init__(bearerFormat=bearerFormat, scheme_name=scheme_name, description=description, auto_error=auto_error)

    async def __call__(self, request: Request):
        creds = await super().__call__(request)

        token = creds.credentials
        
        token_data = decode_token(token)
        
        if await token_in_blocklist(token_data['jti']):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="token has been revoked or expired"
            )

        if not self.token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="token expired or invalid"
            )
        
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
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a valid access token"
            )
        
class RefreshTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict):
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a valid refresh token"
            )
        
async def get_current_user(
        token_details: dict = Depends(AccessTokenBearer()),
        session: AsyncSession = Depends(get_session)):
    user_email = token_details["user"]["email"]
    
    user = await auth_services.get_user_by_email(user_email, session)

    return user
