from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_menu_kb():
    kb = [
        [InlineKeyboardButton(text="Generar Token Canal Gratis", callback_data="generate_free_token")],
        [InlineKeyboardButton(text="Ver Suscripciones VIP", callback_data="view_vip_subs")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)
