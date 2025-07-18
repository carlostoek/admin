# middlewares/logging.py
# Middleware para logging de eventos y errores

from aiogram.dispatcher.middlewares.base import BaseMiddleware
import logging

class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        logging.info(f"Evento recibido: {event}")
        try:
            return await handler(event, data)
        except Exception as e:
            logging.error(f"Error en handler: {e}")
            raise