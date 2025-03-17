from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config
from sqlalchemy.orm import sessionmaker
from src.books.models import Book

async_engine = AsyncEngine(
    create_engine(
        Config.DATABASE_URL,
        echo=True
    )
)

async def initdb():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async_session = sessionmaker(
        bind=async_engine,
        class_=AsyncEngine,
        expire_on_commit=False
    )

    async with async_engine() as session:
        yield session