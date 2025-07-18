# tests/test_db.py
# Test unitario para operaciones de base de datos

import asyncio
from database import init_db, add_user, get_user

async def test_add_and_get_user():
    await init_db()
    await add_user(111, "testuser", "VIP", 9999999999)
    user = await get_user(111)
    assert user[1] == 111
    assert user[2] == "testuser"
    assert user[3] == "VIP"

if __name__ == "__main__":
    asyncio.run(test_add_and_get_user())