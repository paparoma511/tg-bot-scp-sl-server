from aiogram import types
from aiogram.filters import Command
from database.memory import user_cards

@dp.message(Command("cards"))
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