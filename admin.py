from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from config import ADMINS
from database import db

router = Router()


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