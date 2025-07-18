# handlers/vip.py
# Manejo de suscripciones y acceso al canal VIP

from aiogram import Router, types, F
from aiogram.filters import CommandStart
from database import get_token, use_token, add_user, update_user_role
from config import settings
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta

router = Router()

@router.message(CommandStart(deep_link=True))
async def process_vip_token(message: types.Message, command: CommandStart):
    token = command.args
    token_data = await get_token(token)
    if not token_data or token_data[7]:  # used_by
        await message.answer("Token inválido o ya usado.")
        return
    # Asignar rol VIP y calcular expiración
    duration_days = token_data[4]
    expiry = int((datetime.now() + timedelta(days=duration_days)).timestamp())
    await add_user(message.from_user.id, message.from_user.username, "VIP", expiry)
    await use_token(token, message.from_user.id)
    # Enviar invitación nativa
    invite_link = await message.bot.create_chat_invite_link(settings.VIP_CHANNEL_ID, member_limit=1, expire_date=expiry)
    await message.answer(f"¡Bienvenido VIP! Únete aquí: {invite_link.invite_link}")

@router.message(Command("renew"))
async def renew_vip(message: types.Message):
    await message.answer("Contacta a un administrador para renovar tu suscripción VIP.")

# REF: database.py add_user, use_token, update_user_role