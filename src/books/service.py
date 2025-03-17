from src.books.schemas import CreateBookModel, BookUpdateModel
from sqlalchemy.ext.asyncio import AsyncSession
from src.books.models import Book
from datetime import datetime
from sqlmodel import select, desc

class BookService:

    async def create_book(self, book_data: CreateBookModel, session: AsyncSession):
        book_data_dict = book_data.model_dump()

        new_book = Book(
            **book_data_dict
        )
        new_book.published_date = datetime.strptime(new_book.published_date, "%Y-%m-%d")

        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book
    
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        results = await session.execute(statement)
        books = results.scalars().all()
        return books
    
    async def get_book(self, book_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.execute(statement)
        book = result.scalar()
        return book if book is not None else None
    
    async def update_book(self, book_uid: str, updated_book_data: BookUpdateModel, session: AsyncSession):
        db_book = await self.get_book(book_uid, session)

        if db_book is not None:
            updated_book_data_dict = updated_book_data.model_dump()

            for k,v in updated_book_data_dict.items():
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