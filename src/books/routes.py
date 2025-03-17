from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from src.books.book_data import books
from src.books.schemas import Book, BookUpdateModel, CreateBookModel
from src.db.main import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from sqlalchemy.ext.asyncio.session import AsyncSession


book_router = APIRouter()
book_service = BookService()

@book_router.get("/")
async def get_all_books(session: AsyncSession = Depends(get_session)):
    results = await book_service.get_all_books(session)
    return results

@book_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: CreateBookModel, session: AsyncSession = Depends(get_session)):
    result = await book_service.create_book(book_data, session)
    return result


@book_router.get("/{book_uid}")
async def get_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    result = await book_service.get_book(book_uid, session)
    
    if result is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    return result

@book_router.patch("/{book_uid}")
async def update_book(book_uid: str, book_update_data:BookUpdateModel, session: AsyncSession = Depends(get_session)):

    result = await book_service.update_book(book_uid, book_update_data, session)
    
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    return result

@book_router.delete("/{book_uid}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    
    result = await book_service.delete_book(book_uid, session)

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    return {"ok": True}