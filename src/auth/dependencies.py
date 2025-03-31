from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException, status
from src.auth.auth import decode_token
from src.auth.redis import token_in_blocklist

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