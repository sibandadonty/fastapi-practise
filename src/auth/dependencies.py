from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException, status
from src.auth.main import decode_token
from src.auth.redis import token_in_blocklist

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
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token"
            )
        
class RefreshTokenBearer(TokenBearer):
    def verify_token_details(self, token_details):
        if token_details and not token_details["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a refresh token"
            )