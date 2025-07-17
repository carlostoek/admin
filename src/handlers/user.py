from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import User

user_router = Router()

@user_router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("¡Hola! Soy tu bot.")

async def check_vip_status(session: AsyncSession, telegram_id: int):
    """
    Verifica el estado VIP de un usuario por su telegram_id.
    """
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    return user
