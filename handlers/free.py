# handlers/free.py
# Manejo de solicitudes y acceso al canal gratuito

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
import logging
import os
from config import settings
from database import add_user, get_user, update_user_role
from utils.scheduler import schedule_free_acceptance

router = Router()

@router.message(Command("free"))
async def request_free_access(message: types.Message):
    # Verificar si ya es miembro
    try:
        member = await message.bot.get_chat_member(settings.FREE_CHANNEL_ID, message.from_user.id)
        if member.status in ['member', 'administrator', 'creator']:
            await message.answer("✅ Ya eres miembro del canal gratuito.")
            return
    except Exception as e:
        logging.error(f"Error al verificar membresía: {e}")

    # Registrar usuario
    await add_user(message.from_user.id, message.from_user.username, "FREE_PENDING")
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📌 Solicitar acceso", callback_data="request_free")],
        [InlineKeyboardButton(text="📢 Ver reglas", url=settings.FREE_CHANNEL_RULES_URL)]
    ])
    
    await message.answer(
        "🔓 Solicitud de acceso al canal gratuito\n\n"
        "📌 Tu solicitud será procesada en breve.\n"
        "⏳ Tiempo estimado: {} minutos\n\n"
        "👉 Por favor lee las reglas antes de unirte:".format(
            int(os.getenv("FREE_CHANNEL_DELAY", 5))),
        reply_markup=kb
    )

@router.callback_query(F.data == "request_free")
async def process_free_request(call: types.CallbackQuery):
    user = await get_user(call.from_user.id)
    if not user or user[3] != "FREE_PENDING":
        await call.answer("❌ Ya tienes una solicitud en proceso o no has usado /free")
        return
    
    await call.answer("✅ Solicitud recibida correctamente")
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(
        "⏳ Tu solicitud está siendo procesada...\n"
        "Recibirás el enlace de acceso cuando sea aprobada."
    )
    
    # Programar aceptación automática
    await schedule_free_acceptance(call.from_user.id, call.bot)

@router.message(Command("mystatus"))
async def check_free_status(message: types.Message):
    user = await get_user(message.from_user.id)
    if not user:
        await message.answer("❌ No tienes ninguna solicitud registrada. Usa /free para solicitar acceso.")
        return
    
    status_messages = {
        "FREE_PENDING": "🕒 Tu solicitud está pendiente de aprobación",
        "FREE": "✅ Ya tienes acceso al canal gratuito",
        "VIP": "⭐ Eres usuario VIP (usa /myvip para detalles)"
    }
    
    status = user[3]  # user[3] es el rol
    await message.answer(status_messages.get(status, "❓ Estado desconocido. Contacta al administrador."))

# Middleware para verificar nuevos miembros en el canal gratis
@router.chat_join_request()
async def handle_join_request(update: types.ChatJoinRequest):
    if update.chat.id == settings.FREE_CHANNEL_ID:
        await update.approve()  # Aprobar automáticamente
        await update.bot.send_message(
            update.from_user.id,
            f"🎉 ¡Bienvenido al canal {update.chat.title}!\n\n"
            "Ahora puedes acceder a todo el contenido gratuito.\n"
            "Usa /help para ver los comandos disponibles."
        )
        
