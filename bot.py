import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from config import TOKEN
from scp_api import get_server_info

# --- ЛОГИ (ВАЖНО для bothost) ---
logging.basicConfig(level=logging.INFO)

print("BOT FILE STARTED")

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 SCP:SL Bot\n\n"
        "Команда:\n"
        "/server IP:PORT"
    )


@dp.message(Command("server"))
async def server(message: types.Message):
    try:
        args = message.text.split()

        if len(args) < 2:
            await message.answer("❌ Используй: /server IP:PORT")
            return

        ip = args[1]

        await message.answer("🔎 Ищу сервер...")

        data = await get_server_info(ip)

        if not data:
            await message.answer("❌ Сервер не найден")
            return

        await message.answer(
            f"🎮 <b>{data['name']}</b>\n"
            f"📡 Статус: {data['status']}\n"
            f"👥 Онлайн: {data['players']}\n"
            f"🗺 Карта: {data['map']}",
            parse_mode="HTML"
        )

    except Exception as e:
        await message.answer(f"⚠️ Ошибка: {e}")
        print("HANDLER ERROR:", repr(e))


async def main():
    print("STARTING BOT...")

    try:
        # ВАЖНО: убирает старые webhook (часто причина SIGTERM)
        await bot.delete_webhook(drop_pending_updates=True)

        print("BOT IS RUNNING")
        await dp.start_polling(bot)

    except Exception as e:
        print("FATAL ERROR:", repr(e))


if __name__ == "__main__":
    asyncio.run(main())