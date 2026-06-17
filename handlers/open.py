import time
from aiogram import types
from aiogram.filters import Command

from config import ADMINS, COOLDOWN
from database.memory import user_cards, user_last_open
from services.card_system import generate_cards

@dp.message(Command("open"))
async def open_cards(message: types.Message):
    user_id = message.from_user.id
    now = time.time()

    is_admin = user_id in ADMINS

    if not is_admin:
        last = user_last_open.get(user_id, 0)
        if now - last < COOLDOWN:
            remain = COOLDOWN - (now - last)
            h = int(remain // 3600)
            m = int((remain % 3600) // 60)

            await message.answer(f"⏳ КД: {h}ч {m}м")
            return

    cards = generate_cards(2)

    user_cards.setdefault(user_id, [])

    text = "🎁 Ты получил:\n\n"

    for rarity, card in cards:
        user_cards[user_id].append(f"{rarity} {card}")
        text += f"{rarity} → {card}\n"

    user_last_open[user_id] = now

    await message.answer(text)