from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def user_menu_kb():
    kb = [
        [KeyboardButton(text="Solicitar acceso canal gratis")],
        [KeyboardButton(text="Ver estado VIP")],
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)