from aiogram import types
from aiogram.filters import Command

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 SCP:SL Cards Bot\n\n"
        "Команды:\n"
        "/open - открыть 2 карты\n"
        "/cards - твоя коллекция"
    )