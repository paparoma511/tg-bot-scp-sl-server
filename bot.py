import asyncio
import logging

from aiogram import Bot, Dispatcher
from config import BOT_TOKEN

from handlers.start import router as start_router
from handlers.open import router as open_router
from handlers.cards import router as cards_router

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(open_router)
dp.include_router(cards_router)

logging.basicConfig(level=logging.INFO)

async def main():
    print("BOT STARTED")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())