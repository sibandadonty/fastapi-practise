from datetime import datetime
from sqlmodel import select, desc
from .schemas import BookCreateModel, BookUpdateModel
from src.db.main import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.books.models import Books

class BookServices:

    async def create_book(self, book_data: BookCreateModel, session: AsyncSession):
        book = book_data.model_dump()
        new_book = Books(
            **book
        )
        new_book.published_date = datetime.strptime(book_data.published_date, "%Y-%m-%d")
        session.add(new_book)
        await session.commit()
        return new_book
    
    async def get_book(self, book_uid: str, session: AsyncSession):
        statement = select(Books).where(Books.uid == book_uid)
        results = await session.execute(statement)
        book = results.scalar()
        return book if book is not None else None
    
    async def get_all_books(self, session: AsyncSession):
        statement = select(Books).order_by(desc(Books.created_at))
        results = await session.execute(statement)
        return results.scalars().all()
    
    async def update_book(self, book_uid: str, updated_book_data: BookUpdateModel, session: AsyncSession):
        db_book = await self.get_book(book_uid, session)

        if not db_book:
            return None
        else:
            book_data_dict = updated_book_data.model_dump(exclude_unset=True)
            db_book.sqlmodel_update(book_data_dict)
            session.add(db_book)
            await session.commit()
            session.refresh(db_book)
            return db_book
             
        
    async def delete_book(self, book_uid: str, session: AsyncSession):
        db_book = await self.get_book(book_uid, session)
        if not db_book:
            return None
        else:
            await session.delete(db_book)
            await session.commit()
            return {}
