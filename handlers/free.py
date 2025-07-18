# handlers/free.py
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
import os
from datetime import datetime
from config import settings
from database import add_user, get_user
from utils.scheduler import schedule_free_acceptance

# Crear router específico para comandos free
free_router = Router(name="free_router")

@free_router.message(Command("free"))
async def handle_free_command(message: types.Message):
    try:
        # Verificar si ya existe el usuario
        user = await get_user(message.from_user.id)
        if user and user.get("role") in ["FREE", "FREE_PENDING"]:
            await message.answer("🔄 Ya tienes una solicitud de acceso en proceso.")
            return

        # Registrar nuevo usuario
        await add_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            role="FREE_PENDING"
        )

        # Crear teclado de solicitud
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="✅ Solicitar acceso",
                callback_data="request_free_access"
            )],
            [InlineKeyboardButton(
                text="📜 Ver reglas",
                url=settings.FREE_CHANNEL_RULES_URL
            )]
        ])

        await message.answer(
            "📝 *Solicitud de acceso al canal gratuito*\n\n"
            "🔹 Tu solicitud será procesada en breve\n"
            f"⏳ Tiempo estimado: {os.getenv('FREE_CHANNEL_DELAY', 5)} minutos\n\n"
            "👉 Por favor revisa las reglas antes de solicitar acceso:",
            reply_markup=kb,
            parse_mode="Markdown"
        )

    except Exception as e:
        logging.error(f"Error en comando /free: {e}")
        await message.answer("❌ Ocurrió un error al procesar tu solicitud. Intenta nuevamente.")

@free_router.callback_query(F.data == "request_free_access")
async def handle_free_request(callback: types.CallbackQuery):
    try:
        # Verificar estado del usuario
        user = await get_user(callback.from_user.id)
        if not user or user.get("role") != "FREE_PENDING":
            await callback.answer("⚠️ Primero usa el comando /free", show_alert=True)
            return

        await callback.answer("✅ Solicitud recibida correctamente")
        await callback.message.edit_reply_markup(reply_markup=None)
        
        # Programar aceptación automática
        await schedule_free_acceptance(
            user_id=callback.from_user.id,
            bot=callback.bot
        )

        await callback.message.answer(
            "⏳ *Tu solicitud está siendo procesada*\n\n"
            "Recibirás una notificación cuando sea aprobada.\n"
            "Tiempo estimado: "
            f"{os.getenv('FREE_CHANNEL_DELAY', 5)} minutos",
            parse_mode="Markdown"
        )

    except Exception as e:
        logging.error(f"Error en callback free: {e}")
        await callback.answer("❌ Error al procesar solicitud", show_alert=True)
