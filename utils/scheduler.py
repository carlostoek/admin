# utils/scheduler.py
# Tareas programadas: recordatorios y aceptación automática

import asyncio
from config import settings
from database import get_user, update_user_role
from datetime import datetime
import logging
import os

async def start_scheduler(bot):
    asyncio.create_task(vip_expiry_checker(bot))

async def vip_expiry_checker(bot):
    while True:
        from database import get_vip_users
        vips = await get_vip_users()
        now = int(datetime.now().timestamp())
        for v in vips:
            telegram_id, username, role, vip_expiry, created_at = v[1:6]
            if vip_expiry and now > vip_expiry:
                try:
                    await update_user_role(telegram_id, "EXPIRED")
                    await bot.ban_chat_member(settings.VIP_CHANNEL_ID, telegram_id)
                    await bot.send_message(telegram_id, "Tu suscripción VIP ha expirado y has sido removido del canal.")
                except Exception as e:
                    logging.error(f"Error al expulsar usuario VIP: {e}")
            elif vip_expiry and now > vip_expiry - 86400:
                try:
                    await bot.send_message(telegram_id, "Tu suscripción VIP expira en menos de 24 horas. Renueva para no perder acceso.")
                except Exception as e:
                    logging.error(f"Error al enviar recordatorio: {e}")
        await asyncio.sleep(3600)

async def schedule_free_acceptance(user_id, bot):
    delay = int(os.getenv("FREE_CHANNEL_DELAY", 60))
    await asyncio.sleep(delay)
    try:
        invite_link = await bot.create_chat_invite_link(settings.FREE_CHANNEL_ID, member_limit=1, expire_date=None)
        await bot.send_message(user_id, f"¡Acceso concedido! Únete aquí: {invite_link.invite_link}")
    except Exception as e:
        logging.error(f"Error al invitar usuario free: {e}")