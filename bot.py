import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    print("START COMMAND RECEIVED")
    await message.answer("Бот работает ✅")


@dp.message()
async def echo_handler(message: types.Message):
    print("MESSAGE:", message.text)
    await message.answer(f"Вы написали:\n{message.text}")


async def main():
    print("BOT FILE STARTED")

    if not TOKEN:
        print("ОШИБКА: BOT_TOKEN не найден")
        return

    await bot.delete_webhook(drop_pending_updates=True)

    print("START POLLING")

    await dp.start_polling(
        bot,
        allowed_updates=["message"]
    )


if __name__ == "__main__":
    asyncio.run(main())