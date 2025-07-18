# handlers/vip.py
# Manejo de suscripciones y acceso al canal VIP

from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
import logging
from config import settings
from database import get_token, use_token, add_user, update_user_role, get_user

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
    try:
        invite_link = await message.bot.create_chat_invite_link(
            settings.VIP_CHANNEL_ID, 
            member_limit=1, 
            expire_date=datetime.fromtimestamp(expiry)
        )
        await message.answer(
            f"🎉 ¡Bienvenido VIP! 🎉\n"
            f"🔗 Enlace de acceso: {invite_link.invite_link}\n"
            f"⏳ Tu suscripción expira el: {datetime.fromtimestamp(expiry).strftime('%d/%m/%Y')}\n\n"
            f"Usa /renew para renovar cuando esté por expirar."
        )
    except Exception as e:
        logging.error(f"Error al crear invitación: {e}")
        await message.answer("Error al generar tu acceso. Contacta al administrador.")

@router.message(Command("renew"))
async def renew_vip(message: types.Message):
    user = await get_user(message.from_user.id)
    if not user or user[3] != "VIP":  # user[3] es el rol
        await message.answer("No tienes una suscripción VIP activa.")
        return
    
    expiry_date = datetime.fromtimestamp(user[4]) if user[4] else None
    days_left = (expiry_date - datetime.now()).days if expiry_date else 0
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Contactar Admin", url=f"tg://user?id={settings.ADMIN_IDS.split(',')[0]}")]
    ])
    
    if days_left > 0:
        await message.answer(
            f"📅 Tu suscripción VIP expira en {days_left} días.\n"
            f"💬 Contacta a un administrador para renovar:",
            reply_markup=kb
        )
    else:
        await message.answer(
            "⚠️ Tu suscripción VIP ha expirado.\n"
            "💬 Contacta a un administrador para renovar:",
            reply_markup=kb
        )

@router.message(Command("myvip"))
async def check_vip_status(message: types.Message):
    user = await get_user(message.from_user.id)
    if not user or user[3] != "VIP":
        await message.answer("No tienes una suscripción VIP activa.")
        return
    
    expiry_date = datetime.fromtimestamp(user[4]) if user[4] else None
    if expiry_date:
        days_left = (expiry_date - datetime.now()).days
        await message.answer(
            f"⭐ Estado de tu VIP:\n"
            f"🆔 ID: {user[1]}\n"
            f"👤 Usuario: @{user[2]}\n"
            f"📅 Expiración: {expiry_date.strftime('%d/%m/%Y %H:%M')}\n"
            f"⏳ Días restantes: {days_left}\n\n"
            f"Usa /renew para renovar tu suscripción."
        )
    else:
        await message.answer("Error al verificar tu estado VIP. Contacta al administrador.")
        
