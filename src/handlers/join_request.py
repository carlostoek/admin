from aiogram import Router, types
from src.config import FREE_CHANNEL_ID, ADMIN_IDS

join_request_router = Router()

# Handler para solicitudes de ingreso al canal gratuito
@join_request_router.chat_join_request()
async def handle_join_request(event: types.ChatJoinRequest):
    # Solo procesar solicitudes para el canal gratuito
    if event.chat.id == FREE_CHANNEL_ID:
        # Notificar a los administradores con botones para aprobar o rechazar
        for admin_id in ADMIN_IDS:
            try:
                await event.bot.send_message(
                    admin_id,
                    f"Solicitud de ingreso al canal gratuito de: "
                    f"{event.from_user.full_name} (@{event.from_user.username or 'sin username'}, id: {event.from_user.id})",
                    reply_markup=types.InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                types.InlineKeyboardButton(
                                    text="Aprobar",
                                    callback_data=f"approve_join:{event.chat.id}:{event.from_user.id}"
                                ),
                                types.InlineKeyboardButton(
                                    text="Rechazar",
                                    callback_data=f"reject_join:{event.chat.id}:{event.from_user.id}"
                                ),
                            ]
                        ]
                    )
                )
            except Exception:
                pass
        # Opcional: notificar al usuario que su solicitud está pendiente (si el canal lo permite)
        # No se envía mensaje directo al usuario porque no hay contacto con el bot
