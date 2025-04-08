from fastapi import APIRouter, Depends, status, HTTPException
from .services import BookService
from .schemas import BookCreateModel, BookModel, BookUpdateModel
from src.db.models import Book
from src.db.main import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.auth.dependencies import AccessTokenBearer, RoleChecker

book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["admin", "user"]))

not_found_exp = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Book not found"
)

@book_router.post("/", response_model=BookModel, status_code=status.HTTP_201_CREATED, dependencies=[role_checker])
async def create_book(book_data: BookCreateModel, session: AsyncSession = Depends(get_session), token_details: dict = Depends(access_token_bearer)):
    user_uid = token_details.get("user")["uid"]
    new_book = await book_service.create_book(user_uid, book_data, session)
    return new_book

@book_router.get("/user_books/{user_uid}")
async def get_user_books(user_uid: str, session: AsyncSession = Depends(get_session)):
    user_books = await book_service.get_user_books(user_uid, session)
    return user_books

@book_router.get("/", dependencies=[role_checker])
async def get_all_books(session: AsyncSession = Depends(get_session), token_details: dict = Depends(access_token_bearer)):
    books = await book_service.get_all_books(session)
    return books

@book_router.get("/{book_uid}", dependencies=[role_checker])
async def get_book(book_uid: str, session: AsyncSession = Depends(get_session), token_details: dict = Depends(access_token_bearer)):
    book = await book_service.get_book(book_uid, session)

    if book is None:
        raise not_found_exp
    
    return book

@book_router.patch("/{book_uid}", dependencies=[role_checker])
async def update_book(book_uid: str, book_update_data: BookUpdateModel, session: AsyncSession = Depends(get_session), token_details: dict = Depends(access_token_bearer)):
    updated_book = await book_service.update_book(book_uid, book_update_data, session)

    if updated_book is None:
        raise not_found_exp
    
    return updated_book

@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker])
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session), token_details: dict = Depends(access_token_bearer)):
    result = await book_service.delete_book(book_uid, session)

    if result is None:
        raise not_found_exp

    return {} 