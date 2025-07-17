from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from config import ADMIN_IDS
from keyboards.admin import admin_menu_kb
from utils.token_utils import generate_token, get_token_expiry
from database import get_session
from models.token import Token
from sqlalchemy import select

admin_router = Router()

@admin_router.message(Command("admin"))
async def admin_menu(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("No tienes permisos de administrador.")
        return
    await message.answer("Menú de administración:", reply_markup=admin_menu_kb())

@admin_router.callback_query(F.data == "generate_free_token")
async def generate_free_token_handler(callback: CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("No autorizado", show_alert=True)
        return
    token_str = generate_token()
    expires_at = get_token_expiry(24)
    async for session in get_session():
        token = Token(token=token_str, expires_at=expires_at)
        session.add(token)
        await session.commit()
    bot_username = (await callback.bot.me()).username
    link = f"https://t.me/{bot_username}?start={token_str}"
    await callback.message.answer(f"Token generado:\n{link}\nVálido por 24h.")
    await callback.answer()
    
