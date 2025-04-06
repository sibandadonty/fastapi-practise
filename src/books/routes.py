from fastapi import APIRouter, Depends, status, HTTPException
from .services import BookService
from .schemas import BookCreateModel, BookModel, BookUpdateModel
from src.db.models import Book
from src.db.main import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession

book_router = APIRouter()
book_service = BookService()

not_found_exp = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Book not found"
)

@book_router.post("/", response_model=BookModel, status_code=status.HTTP_201_CREATED)
async def create_book(book_data: BookCreateModel, session: AsyncSession = Depends(get_session)):
    new_book = await book_service.create_book(book_data, session)
    return new_book

@book_router.get("/")
async def get_all_books(session: AsyncSession = Depends(get_session)):
    books = await book_service.get_all_books(session)
    return books

@book_router.get("/{book_uid}")
async def get_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    book = await book_service.get_book(book_uid, session)

    if book is None:
        raise not_found_exp
    
    return book

@book_router.patch("/{book_uid}")
async def update_book(book_uid: str, book_update_data: BookUpdateModel, session: AsyncSession = Depends(get_session)):
    updated_book = await book_service.update_book(book_uid, book_update_data, session)

    if updated_book is None:
        raise not_found_exp
    
    return updated_book

@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    result = await book_service.delete_book(book_uid, session)

    if result is None:
        raise not_found_exp

    return {} 