from fastapi.security import HTTPBearer
from src.auth.utils import verify_token
from fastapi import status, HTTPException, Request

class AccessTokenBearer(HTTPBearer):
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
        return token_data

    async def token_valid(self, token: str):
        token = verify_token(token)

        return token is not None