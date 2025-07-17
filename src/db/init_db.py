import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from src.db.models import Base, User
from src.models.token import Token
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost:5432/mydb")

async def init_db():
    """
    Crea todas las tablas necesarias en la base de datos si no existen.
    """
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_db())