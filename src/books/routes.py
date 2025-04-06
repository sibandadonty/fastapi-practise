from fastapi import APIRouter
from .services import BookService
from .schemas import BookCreateModel, BookModel, BookUpdateModel
from src.db.models import Book

book_router = APIRouter()
book_service = BookService()

@book_router.post("/", response_model=BookModel)
async def create_book():
    pass