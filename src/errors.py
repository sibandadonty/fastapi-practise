from typing import Any, Callable
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi import FastAPI


class BooklyException(Exception):
    """This is the base class for all bookly errors"""
    pass

class InvalidToken(BooklyException):
    """User has provided an invalid or expired token"""
    pass

class RevokedToken(BooklyException):
    """User has provided a token that has been revoked"""
    pass

class AccessTokenRequired(BooklyException):
    """User has provided a refresh token when an access token is needed"""
    pass

class RefreshTokenRequired(BooklyException):
    """User has provided an access token when a refresh token is needed"""
    pass

class UserAlreadyExists(BooklyException):
    """User has provided an email for a user who exists during sign up."""
    pass

class InvalidCredentials(BooklyException):
    """User has provided wrong email or password during log in."""
    pass

class InsufficientPermission(BooklyException):
    """User does not have the necessary permissions to perform an action."""
    pass

class BookNotFound(BooklyException):
    """Book Not found"""
    pass

class TagNotFound(BooklyException):
    """Tag Not found"""
    pass

class TagAlreadyExists(BooklyException):
    """Tag already exists"""
    pass

class UserNotFound(BooklyException):
    """User Not found"""
    pass

def create_exception_handler(status_code: int, initial_detail: Any):

    async def exception_handler(request: Request, exe: Exception):
        raise HTTPException(
            status_code=status_code,
            detail=initial_detail
        )
    
    return exception_handler

def register_error_handlers(app: FastAPI):
    app.add_exception_handler(
        BookNotFound, 
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "book not found",
                "error_code": "book_not_found"
            }
        ))
    
    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Please provide a valid access token",
                "resolution": "Please get an access token",
                "error_code": "access_token_required",
            },
        ),
    )

    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Please provide a valid refresh token",
                "resolution": "Please get an refresh token",
                "error_code": "refresh_token_required",
            },
        ),
    )

    @app.exception_handler(500)
    def internal_server_error(request, exe):
        return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content="Ooop something went wrong with the server"
        )