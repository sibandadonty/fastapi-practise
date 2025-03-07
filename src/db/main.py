from sqlmodel import SQLModel, create_engine, text
from src.config import settings
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

engine = AsyncEngine(
    create_engine(settings.DATABASE_URL)
)

async def init_db():
    async with engine.begin() as conn:
        from src.db.models import Books
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with async_session() as session:
        yield session

