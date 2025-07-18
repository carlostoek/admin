# main.py
# Punto de entrada del bot de Telegram para gestión de canales VIP y gratuitos

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from config import settings
from handlers import vip, free, common
from middlewares.logging import LoggingMiddleware
from utils.scheduler import start_scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

async def main():
    bot = Bot(token=settings.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.update.middleware(LoggingMiddleware())

    dp.include_router(common.router)
    dp.include_router(vip.router)
    dp.include_router(free.router)

    await start_scheduler(bot)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())