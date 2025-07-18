# admin_panel.py
# Funciones y comandos de administración para el bot

from aiogram import Router, types, F
from aiogram.filters import Command
from config import settings
from database import get_vip_users, add_token
from utils.tokens import generate_token
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

def is_admin(user_id):
    return str(user_id) in settings.ADMIN_IDS.split(',')

@router.message(Command("admin"))
async def admin_panel(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("No tienes permisos de administrador.")
        return
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Generar Token VIP", callback_data="gen_token")],
        [InlineKeyboardButton(text="Ver VIPs", callback_data="list_vips")]
    ])
    await message.answer("Panel de administración:", reply_markup=kb)

@router.callback_query(F.data == "gen_token")
async def gen_token_callback(call: types.CallbackQuery, state):
    await call.message.answer("Envíame el nombre del token, precio y duración (días) separados por coma.\nEjemplo: <b>VIP Mensual,100,30</b>")
    await state.set_state("await_token_data")

@router.message(F.text, state="await_token_data")
async def process_token_data(message: types.Message, state):
    try:
        name, price, duration = message.text.split(",")
        price = int(price)
        duration = int(duration)
        token = generate_token()
        await add_token(token, name.strip(), price, duration, message.from_user.id)
        await message.answer(f"Token generado: <code>{token}</code>\nLink: https://t.me/{settings.BOT_USERNAME}?start={token}")
        await state.clear()
    except Exception as e:
        await message.answer("Formato incorrecto. Intenta de nuevo.")

@router.callback_query(F.data == "list_vips")
async def list_vips_callback(call: types.CallbackQuery):
    vips = await get_vip_users()
    if not vips:
        await call.message.answer("No hay usuarios VIP.")
        return
    text = "\n".join([f"{v[2]} (ID: {v[1]}) - Expira: {v[4]}" for v in vips])
    await call.message.answer(f"Usuarios VIP:\n{text}")
