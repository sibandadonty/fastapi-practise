from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import create_engine, SQLModel
from .models import Book
from src.config import Config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio.session import AsyncSession

engine = AsyncEngine(
    create_engine(Config.DATABASE_URL)
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as session: 
        yield session
