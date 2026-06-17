import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

load_dotenv()

from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# подключаем хендлеры
import handlers.start
import handlers.open
import handlers.cards

logging.basicConfig(level=logging.INFO)

async def main():
    print("BOT STARTED")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())