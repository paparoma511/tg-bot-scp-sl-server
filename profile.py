from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from database import db

router = Router()


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
        (message.from_user.id,)
    )

    row = cur.fetchone()

    if row is None:
        conn.close()
        await message.answer(
            "❌ Ты ещё не зарегистрирован.\nИспользуй /start"
        )
        return

    cur.execute(
        """
        SELECT COUNT(*)
        FROM cards
        WHERE user_id=?
        """,
        (message.from_user.id,)
    )

    cards_count = cur.fetchone()[0]

    conn.close()

    await message.answer(
        f"👤 {message.from_user.full_name}\n\n"
        f"🃏 Карт: {cards_count}\n"
        f"🎁 Открыто карт: {row[0]}"
    )


@router.message(Command("top"))
async def top(message: Message):

    conn = db()
    cur = conn.cursor()

    cur.execute("""
    SELECT
        users.username,
        users.user_id,
        COUNT(cards.id) AS cards_count
    FROM users
    LEFT JOIN cards
        ON users.user_id = cards.user_id
    GROUP BY users.user_id, users.username
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

        name = f"@{username}" if username else f"ID {user_id}"

        text += f"{place}. {name} — {count} карт\n"

    await message.answer(text)