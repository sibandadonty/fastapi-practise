from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.db.models import Book
from .schemas import BookCreateModel, BookUpdateModel
from datetime import datetime

class BookService:

    async def create_book(self, book_data: BookCreateModel, session: AsyncSession):
        book_data_dict = book_data.model_dump()

        new_book = Book(**book_data_dict)

        new_book.published_date = datetime.strptime(new_book.published_date, "%Y-%m-%d")

        session.add(new_book)

        await session.commit()

        await session.refresh(new_book)

        return new_book
    
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book)

        results = await session.execute(statement)

        books = results.scalars().all()

        return books
    
    async def get_book(self, book_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)

        results = await session.execute(statement)

        book = results.scalar()

        return book if book is not None else None
    
    async def update_book(self, book_uid: str, book_update_data: BookUpdateModel, session: AsyncSession):
        db_book = await self.get_book(book_uid, session)

        if db_book is not None:
            book_update_data_dict = book_update_data.model_dump(exclude_unset=True)

            for k,v in book_update_data_dict.items():
                setattr(db_book, k,v)

            await session.commit()
            await session.refresh(db_book)
            return db_book

        else: 
            return None
        
    async def delete_book(self, book_uid: str, session: AsyncSession):
        db_book = await self.get_book(book_uid, session)

        if db_book is not None:
            await session.delete(db_book)
            await session.commit()
            return {}
        else: 
            return None