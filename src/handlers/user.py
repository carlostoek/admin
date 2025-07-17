from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import User

async def check_vip_status(session: AsyncSession, telegram_id: int):
    """
    Verifica el estado VIP de un usuario por su telegram_id.
    """
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    return user