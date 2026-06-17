import asyncio
import sqlite3
import time

from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import Command

from config import BOT_TOKEN, ADMINS, COOLDOWN
from database import init_db
from cards import get_card
from admin import router as admin_router
from profile import router as profile_router

router = Router()

bot = Bot(BOT_TOKEN)
dp = Dispatcher()
dp.include_router(cards_router)
dp.include_router(profile_router)
dp.include_router(admin_router)

init_db()


def db():
    return sqlite3.connect("cards.db")


# START

@router.message(Command("start"))
async def start(message: Message):
    conn = db()
    cur = conn.cursor()

    cur.execute(
        "INSERT OR IGNORE INTO users(user_id,username) VALUES(?,?)",
        (
            message.from_user.id,
            message.from_user.username
        )
    )

    conn.commit()
    conn.close()

    await message.answer(
        "🎴 SCP:SL Карты, доступные вам команды:\n\n"
        "/open\n"
        "/cards\n"
        "/profile\n"
        "/top\n"
        "/info"
    )


# OPEN

@router.message(Command("open"))
async def open_cards(message: Message):

    conn = db()
    cur = conn.cursor()

    user_id = message.from_user.id

    cur.execute(
        "SELECT last_open FROM users WHERE user_id=?",
        (user_id,)
    )

    row = cur.fetchone()

    now = int(time.time())

    if row:

        last_open = row[0]

        if (
            user_id not in ADMINS
            and
            now - last_open < COOLDOWN
        ):
            left = COOLDOWN - (now - last_open)

            hours = left // 3600

            await message.answer(
                f"⏳ Жди ещё {hours} часов"
            )

            conn.close()
            return

    cards = []

    for _ in range(2):

        rarity, card = get_card()

        cards.append(f"{rarity} | {card}")

        cur.execute(
            """
            INSERT INTO cards(
                user_id,
                rarity,
                card_name
            )
            VALUES(?,?,?)
            """,
            (
                user_id,
                rarity,
                card
            )
        )

    cur.execute(
        """
        UPDATE users
        SET last_open=?,
            cards_opened=cards_opened+2
        WHERE user_id=?
        """,
        (
            now,
            user_id
        )
    )

    conn.commit()
    conn.close()

    await message.answer(
        "🎁 Выпало:\n\n"
        + "\n".join(cards)
    )


# CARDS

@router.message(Command("cards"))
async def cards(message: Message):

    conn = db()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT rarity,card_name
        FROM cards
        WHERE user_id=?
        """,
        (
            message.from_user.id,
        )
    )

    cards = cur.fetchall()

    conn.close()

    if not cards:
        await message.answer("У тебя нет карт")
        return

    text = "🃏 Коллекция:\n\n"

    for rarity, card in cards:
        text += f"{rarity} • {card}\n"

    await message.answer(text)


# PROFILE

@router.message(Command("profile"))
async def profile(message: Message):

    conn = db()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT cards_opened
        FROM users
        WHERE user_id=?
        """,
        (
            message.from_user.id,
        )
    )

    row = cur.fetchone()

    cur.execute(
        """
        SELECT COUNT(*)
        FROM cards
        WHERE user_id=?
        """,
        (
            message.from_user.id,
        )
    )

    cards_count = cur.fetchone()[0]

    conn.close()

    await message.answer(
        f"👤 {message.from_user.full_name}\n\n"
        f"🃏 Карт: {cards_count}\n"
        f"🎁 Открыто карт: {row[0]}"
    )


# TOP

@router.message(Command("top"))
async def top(message: Message):

    conn = db()
    cur = conn.cursor()

    cur.execute("""
    SELECT
        users.username,
        users.user_id,
        COUNT(cards.id) as cards_count
    FROM users
    LEFT JOIN cards
        ON users.user_id = cards.user_id
    GROUP BY users.user_id
    ORDER BY cards_count DESC
    LIMIT 10
    """)

    data = cur.fetchall()

    conn.close()

    if not data:
        await message.answer("🏆 Топ пока пуст.")
        return

    text = "🏆 Топ игроков\n\n"

    for place, (username, user_id, count) in enumerate(data, start=1):

        if username:
            name = f"@{username}"
        else:
            name = f"ID {user_id}"

        text += f"{place}. {name} — {count} карт\n"

    await message.answer(text)


# INFO

@router.message(Command("info"))
async def info(message: Message):

    await message.answer(
        "🎮 Сервер: IMPERIAL || NORULES\n"
        "🌐 IP: 31.25.244.233:7777\n"
        "📦 Версия: 14.2.7\n"
        "💬 Discord: https://discord.gg/vT3WPjGBA2\n"
        "🟢 Статус: Онлайн"
    )


# ADMIN GIVECARD

@router.message(Command("givecard"))
async def givecard(message: Message):

    if message.from_user.id not in ADMINS:
        return

    args = message.text.split(maxsplit=2)

    if len(args) < 3:
        await message.answer(
            "/givecard user_id карта"
        )
        return

    target = int(args[1])
    card = args[2]

    conn = db()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO cards(
        user_id,
        rarity,
        card_name
        )
        VALUES(?,?,?)
        """,
        (
            target,
            "Admin",
            card
        )
    )

    conn.commit()
    conn.close()

    await message.answer("✅ Карта выдана")


dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
   