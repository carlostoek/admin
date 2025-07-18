import aiosqlite
import logging
from config import settings
from pathlib import Path

DB_PATH = Path(settings.DATABASE_URL)

async def init_db():
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            # Tabla users
            await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE,
                username TEXT,
                role TEXT CHECK(role IN ('VIP', 'FREE', 'FREE_PENDING', 'EXPIRED', 'ADMIN')),
                vip_expiry INTEGER,
                created_at INTEGER DEFAULT (strftime('%s', 'now'))
            )
            """)
            
            # Tabla tokens
            await db.execute("""
            CREATE TABLE IF NOT EXISTS tokens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                token TEXT UNIQUE,
                name TEXT,
                price INTEGER,
                duration INTEGER,
                created_by INTEGER,
                created_at INTEGER DEFAULT (strftime('%s', 'now')),
                used_by INTEGER DEFAULT NULL,
                used_at INTEGER DEFAULT NULL,
                FOREIGN KEY (created_by) REFERENCES users(telegram_id),
                FOREIGN KEY (used_by) REFERENCES users(telegram_id)
            )
            """)
            
            # Índices para mejor performance
            await db.execute("CREATE INDEX IF NOT EXISTS idx_users_role ON users(role)")
            await db.execute("CREATE INDEX IF NOT EXISTS idx_users_vip_expiry ON users(vip_expiry)")
            await db.execute("CREATE INDEX IF NOT EXISTS idx_tokens_used ON tokens(used_by)")
            
            await db.commit()
            logging.info("Base de datos inicializada correctamente")
    except Exception as e:
        logging.error(f"Error al inicializar DB: {e}")
        raise

async def add_user(telegram_id, username, role, vip_expiry=None):
    from time import time
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO users (telegram_id, username, role, vip_expiry, created_at) VALUES (?, ?, ?, ?, ?)",
            (telegram_id, username, role, vip_expiry, int(time()))
        )
        await db.commit()

async def get_user(telegram_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)) as cursor:
            return await cursor.fetchone()

async def update_user_role(telegram_id, role, vip_expiry=None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET role = ?, vip_expiry = ? WHERE telegram_id = ?",
            (role, vip_expiry, telegram_id)
        )
        await db.commit()

async def get_vip_users():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users WHERE role = 'VIP'",) as cursor:
            return await cursor.fetchall()

async def add_token(token, name, price, duration, created_by):
    from time import time
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO tokens (token, name, price, duration, created_by, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (token, name, price, duration, created_by, int(time()))
        )
        await db.commit()

async def get_token(token):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM tokens WHERE token = ?", (token,)) as cursor:
            return await cursor.fetchone()

async def use_token(token, user_id):
    from time import time
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE tokens SET used_by = ?, used_at = ? WHERE token = ?",
            (user_id, int(time()), token)
        )
        await db.commit()
