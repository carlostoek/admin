from aiogram import Router, types, F
from src.config import ADMIN_IDS

admin_join_approval_router = Router()

# Handler para callbacks de aprobación/rechazo de solicitudes de ingreso
@admin_join_approval_router.callback_query(F.data.startswith("approve_join:"))
async def approve_join_callback(callback: types.CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("No autorizado", show_alert=True)
        return
    _, chat_id, user_id = callback.data.split(":")
    chat_id = int(chat_id)
    user_id = int(user_id)
    try:
        await callback.bot.approve_chat_join_request(chat_id, user_id)
        await callback.answer("Solicitud aprobada.")
        await callback.message.edit_text("Solicitud aprobada.")
    except Exception as e:
        await callback.answer("Error al aprobar.", show_alert=True)

@admin_join_approval_router.callback_query(F.data.startswith("reject_join:"))
async def reject_join_callback(callback: types.CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer("No autorizado", show_alert=True)
        return
    _, chat_id, user_id = callback.data.split(":")
    chat_id = int(chat_id)
    user_id = int(user_id)
    try:
        await callback.bot.decline_chat_join_request(chat_id, user_id)
        await callback.answer("Solicitud rechazada.")
        await callback.message.edit_text("Solicitud rechazada.")
    except Exception as e:
        await callback.answer("Error al rechazar.", show_alert=True)
      
