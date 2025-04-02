from typing import Any
from fastapi import Request, FastAPI, status
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


def register_exception_handlers(app: FastAPI):

    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_details={
                "message": "an invalid refresh token",
                "error_code": "invalid_refresh_token"
            }
        )
    )

    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_details={
                "message": "an invalid access token was provided",
                "error_code": "invalid_access_token"
            }
        )
    )

    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_details={
                "message": "the provided token is invalid or expired or revoked",
                "error_code": "invalid_token"
            }
        )
    )

    app.add_exception_handler(
        InvalidEmailOrPassword,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_details={
                "message": "the provided email or password is invalid",
                "error_code": "invalid_credentials"
            }
        )
    )

    app.add_exception_handler(
        UserAlreadyExist,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_details={
                "message": "the provided email already has an account register",
                "error_code": "user_already_exist"
            }
        )
    )
