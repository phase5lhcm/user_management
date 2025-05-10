from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import Database

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async_session = Database.get_session_factory()
    async with async_session() as session:
        yield session
