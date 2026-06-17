import asyncio
import logging
import time
import random
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from dotenv import load_dotenv
import os

load_dotenv()

# =====================
# ⚙ НАСТРОЙКИ
# =====================
BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMINS = [123456789]  # <-- твой ID
COOLDOWN = 60 * 60 * 24

# =====================
# 🃏 КАРТЫ И РЕДКОСТИ
# =====================
CARDS = {
    "🟢 Common": ["Class-D", "Scientist", "Guard", "Medkit"],
    "🔵 Rare": ["MTF Private", "Chaos Rifleman", "Keycard L2"],
    "🟣 Epic": ["SCP-173", "SCP-049", "E-11 Rifle"],
    "🟡 Legendary": ["SCP-096", "SCP-106", "Micro H.I.D."],
    "🔴 Mythic": ["SCP-682", "SCP-999", "SCP-001"]
}

WEIGHTS = {
    "🟢 Common": 60,
    "🔵 Rare": 25,
    "🟣 Epic": 10,
    "🟡 Legendary": 4,
    "🔴 Mythic": 1
}

# =====================
# 💾 ПАМЯТЬ
# =====================
user_cards = {}
user_last_open = {}

# =====================
# 🎲 ЛОГИКА
# =====================
def roll_rarity():
    pool = []
    for r, w in WEIGHTS.items():
        pool.extend([r] * w)
    return random.choice(pool)


def generate_cards(n=2):
    result = []
    for _ in range(n):
        rarity = roll_rarity()
        card = random.choice(CARDS[rarity])
        result.append((rarity, card))
    return result

# =====================
# 🤖 BOT
# =====================
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()

# =====================
# /start
# =====================
@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 SCP Card Bot\n\n"
        "/open - открыть 2 карты\n"
        "/cards - коллекция"
    )

# =====================
# /open
# =====================
@router.message(Command("open"))
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

# =====================
# /cards
# =====================
@router.message(Command("cards"))
async def cards(message: types.Message):
    user_id = message.from_user.id
    cards = user_cards.get(user_id, [])

    if not cards:
        await message.answer("🃏 У тебя нет карт")
        return

    text = "🃏 ТВОЯ КОЛЛЕКЦИЯ:\n\n"
    for c in cards:
        text += f"• {c}\n"

    await message.answer(text)

# =====================
# MAIN
# =====================
async def main():
    logging.basicConfig(level=logging.INFO)

    dp.include_router(router)

    print("BOT STARTED")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())