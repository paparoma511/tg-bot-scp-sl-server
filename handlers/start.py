from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 SCP Card Bot\n\n"
        "/open - открыть 2 карты\n"
        "/cards - твоя коллекция"
    )