from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from ..keyboards.user import user_menu_kb
from ..database import get_session
from ..models.token import Token
from ..models.user import User
from ..config import FREE_CHANNEL_ID, VIP_CHANNEL_ID
from sqlalchemy.future import select
from datetime import datetime

user_router = Router()

 @user_router.message(CommandStart())
async def start(message: Message, command: CommandStart.CommandObject):
    token = command.args
    if token:
        async for session in get_session():
            result = await session.execute(select(Token).where(Token.token == token, Token.is_used == False))
            token_obj = result.scalar_one_or_none()
            if token_obj and (not token_obj.expires_at or token_obj.expires_at > datetime.utcnow()):
                token_obj.is_used = True
                user_result = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
                user = user_result.scalar_one_or_none()
                if not user:
                    user = User(telegram_id=message.from_user.id)
                    session.add(user)
                token_obj.user = user
                await session.commit()
                await message.answer("¡Acceso concedido al canal gratuito! Únete aquí: https://t.me/c/{}/".format(str(FREE_CHANNEL_ID)[4:]))
                return
            else:
                await message.answer("Token inválido o expirado.")
                return
    await message.answer("Bienvenido. Usa el menú para interactuar.", reply_markup=user_menu_kb())

 @user_router.message(F.text == "Solicitar acceso canal gratis")
async def request_free_channel(message: Message):
    await message.answer("Solicita un token a un administrador para acceder al canal gratuito.")

 @user_router.message(F.text == "Ver estado VIP")
async def check_vip_status(message: Message):
    async for session in get_session():
        result = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
        user = result.scalar_one_or_none()
        if user and user.is_vip and user.vip_expiry and user.vip_expiry > datetime.utcnow():
            await message.answer(f"Eres VIP hasta {user.vip_expiry.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            await message.answer("No tienes suscripción VIP activa.")