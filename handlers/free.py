from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
import os
from config import settings
from database import add_user, get_user
from utils.scheduler import schedule_free_acceptance

free_router = Router(name="free_router")

@free_router.message(Command("free"))
async def request_free_access(message: types.Message):
    try:
        user = await get_user(message.from_user.id)
        
        if user:
            if user[3] in ['FREE', 'FREE_PENDING']:
                await message.answer("🔄 Ya tienes una solicitud de acceso en proceso.")
                return
            elif user[3] == 'VIP':
                await message.answer("⭐ Ya eres usuario VIP, no necesitas acceso gratuito.")
                return

        success = await add_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            role="FREE_PENDING"
        )
        
        if not success:
            await message.answer("❌ Error al registrar tu solicitud. Intenta nuevamente.")
            return

        # Teclado inline corregido - solo botones con callback_data o URL
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Solicitar acceso", 
                    callback_data="request_free"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📜 Ver reglas",
                    url=settings.FREE_CHANNEL_RULES_URL
                )
            ]
        ])

        await message.answer(
            "📝 Solicitud de acceso al canal gratuito\n\n"
            "🔹 Tu solicitud será procesada en breve\n"
            f"⏳ Tiempo estimado: {os.getenv('FREE_CHANNEL_DELAY', 5)} minutos\n\n"
            "👉 Por favor revisa las reglas antes de solicitar acceso:",
            reply_markup=kb
        )

    except Exception as e:
        logging.error(f"Error en comando /free: {str(e)}", exc_info=True)
        await message.answer("❌ Ocurrió un error al procesar tu solicitud. Intenta nuevamente.")

@free_router.callback_query(F.data == "request_free")
async def process_free_request(callback: types.CallbackQuery):
    try:
        user = await get_user(callback.from_user.id)
        if not user or user[3] != 'FREE_PENDING':
            await callback.answer("⚠️ Primero usa el comando /free", show_alert=True)
            return

        await callback.answer("✅ Solicitud recibida correctamente")
        await callback.message.edit_reply_markup(reply_markup=None)
        
        await schedule_free_acceptance(callback.from_user.id, callback.bot)
        
        await callback.message.answer(
            "⏳ Tu solicitud está siendo procesada...\n"
            f"Tiempo estimado: {os.getenv('FREE_CHANNEL_DELAY', 5)} minutos"
        )

    except Exception as e:
        logging.error(f"Error en callback free: {str(e)}", exc_info=True)
        await callback.answer("❌ Error al procesar solicitud", show_alert=True)
        
