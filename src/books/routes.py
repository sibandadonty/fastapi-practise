from fastapi import HTTPException, status, APIRouter, Depends
from src.books.schemas import Book, BookCreateModel, BookUpdateModel
from src.books.services import BookServices
from src.db.main import get_session
from typing import List
from sqlalchemy.ext.asyncio.session import AsyncSession

book_router = APIRouter()
book_services = BookServices()

not_found_exp = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Book not found"
)

@book_router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book_data: BookCreateModel, session: AsyncSession =Depends(get_session)):
    book = await book_services.create_book(book_data, session)
    return book

@book_router.get("/", response_model=List[Book])
async def get_all_books(session: AsyncSession = Depends(get_session)):
    books = await book_services.get_all_books(session)
    return books

@book_router.get("/{book_uid}", response_model=Book)
async def get_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    book = await book_services.get_book(book_uid, session)
    if not book:
        raise not_found_exp
    return book

@book_router.patch("/{book_uid}", response_model=Book)
async def update_book(book_uid: str, book_update_data: BookUpdateModel, session: AsyncSession = Depends(get_session)):
    book = await book_services.update_book(book_uid, book_update_data, session)
    if book is None: 
        raise not_found_exp
    return book

@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    result = await book_services.delete_book(book_uid, session)
    if result is None:
        raise not_found_exp
    return {"ok": True}