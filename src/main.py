import asyncio
from aiogram import Bot, Dispatcher
from src.db.init_db import init_db

API_TOKEN = "TU_TOKEN_DE_BOT"

async def main():
    # Inicializa la base de datos (crea tablas si no existen)
    await init_db()

    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    # Aquí iría el registro de handlers, middlewares, etc.

    # Inicia el polling del bot
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())