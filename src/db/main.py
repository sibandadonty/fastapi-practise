from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.config import Config
from sqlalchemy.orm import sessionmaker
from src.books.models import Club

async_engine = AsyncEngine(create_engine(Config.DATABASE_URL))

async def init_db():
    async with async_engine.begin() as conn:
       await conn.run_sync(SQLModel.metadata.create_all)      

async def get_session():
    async_session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async with async_engine() as session:
        yield session
