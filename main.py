# main.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from config import settings
from database import init_db
from handlers import vip, free, common
from middlewares.logging import LoggingMiddleware
from utils.scheduler import start_scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

async def main():
    # Inicializar base de datos primero
    await init_db()
    
    # Configuración moderna del bot
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    dp = Dispatcher(storage=MemoryStorage())
    dp.update.middleware(LoggingMiddleware())

    dp.include_router(free.router)
    dp.include_router(common.router)
    dp.include_router(vip.router)
    

    await start_scheduler(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
