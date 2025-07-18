# handlers/common.py
# Comandos y mensajes comunes

from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer("¡Bienvenido! Usa /free para solicitar acceso gratuito o solicita un token VIP a un administrador.")

@router.message(Command("help"))
async def help_cmd(message: types.Message):
    await message.answer("Comandos disponibles:\n/free - Solicitar acceso gratuito\n/start - Inicio\n/help - Ayuda")