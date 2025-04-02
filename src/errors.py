from typing import Any
from fastapi import Request
from fastapi.responses import JSONResponse

class ClublyException(Exception):
    """This is the base class for all clubly exceptions"""
    pass

class RefreshTokenRequired(ClublyException):
    """User has provided an access token when a refresh token is required"""
    pass

class AccessTokenRequired(ClublyException):
    """User has provided a refresh token when an access token is required"""
    pass

class InvalidToken(ClublyException):
    """The token provided is invalid"""
    pass

class InvalidEmailOrPassword(ClublyException):
    """The provided email or password is invalid"""
    pass

class UserAlreadyExist(ClublyException):
    """The email provided during registration already has an existing account created"""
    pass

def create_exception_handler(status_code: int, initial_details: Any):

    async def exception_handler(request: Request, exc: ClublyException):

        return JSONResponse(
            status_code=status_code,
            content=initial_details
        )
    
    return exception_handler


    