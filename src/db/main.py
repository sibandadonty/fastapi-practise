from sqlmodel import SQLModel, create_engine, text
from src.config import settings
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession

engine = AsyncEngine(
    create_engine(settings.DATABASE_URL, echo=True)
)

async def init_db():
    async with engine.begin() as conn:
        from src.books.models import Books
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    Session = AsyncSession(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with Session() as session:
        yield session

