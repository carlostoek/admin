import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, BigInteger, Boolean, DateTime
import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost:5432/mydb")

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    is_vip = Column(Boolean, default=False)
    vip_expiry = Column(DateTime)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

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