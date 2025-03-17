from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config

async_engine = AsyncEngine(
    create_engine(
        Config.DATABASE_URL,
        echo=True
    )
)

async def initdb():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)