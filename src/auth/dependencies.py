from fastapi.security import HTTPBearer
from src.auth.utils import verify_token
from fastapi import status, HTTPException, Request

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request):
        creds = await super().__call__(request)
        
        token = creds.credentials
        
        token_data = verify_token(token)
        
        if not self.token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "Token is expired or invalid",
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