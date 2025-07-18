# handlers/free.py
# Manejo de solicitudes y acceso al canal gratuito

from aiogram import Router, types, F
from config import settings
from database import add_user
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.scheduler import schedule_free_acceptance

router = Router()

@router.message(Command("free"))
async def request_free_access(message: types.Message):
    await add_user(message.from_user.id, message.from_user.username, "FREE")
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Solicitar acceso", callback_data="request_free")]
    ])
    await message.answer("¿Deseas solicitar acceso al canal gratuito?", reply_markup=kb)

@router.callback_query(F.data == "request_free")
async def process_free_request(call: types.CallbackQuery):
    # Programar aceptación automática según delay configurado
    await call.message.answer("Tu solicitud ha sido recibida. Serás aceptado pronto.")
    await schedule_free_acceptance(call.from_user.id, call.bot)

# REF: database.py add_user