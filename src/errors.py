from fastapi import Request, FastAPI, status
from fastapi.responses import JSONResponse

class BooklyException(Exception):
    """This is the base class for all bookly exceptions"""

class UserNotFound(BooklyException):
    "User not found"

class AccessTokenRequired(BooklyException):
    "User provided a refresh token where an access token is required"

class RefreshTokenRequired(BooklyException):
    """User provided an access token where a refresh token is required"""

def create_exception_handler(status_code: int, initial_details: dict):

    async def exception_handler(request: Request, exc: BooklyException):

        return JSONResponse(
            status_code=status_code,
            content=initial_details
        )
    return exception_handler

def register_exception_handlers(app: FastAPI):

    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_details={
                "message": "User not found",
                "error_code": "user_not_found"
            }
        )
    )

    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_details={
                "message": "Provide a valid access token",
                "error_code": "invalid_access_token"
            }
        )
    )

    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_details={
                "message": "Provide a valid refresh token",
                "error_code": "invalid refresh token"
            }
        )
    )