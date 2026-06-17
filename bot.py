import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from dotenv import load_dotenv

from scp_api import get_server_info

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        "👋 SCP:SL Monitor Bot\n\n"
        "Использование:\n"
        "/server IP:PORT"
    )


@dp.message(Command("server"))
async def server_handler(message: types.Message):
    args = message.text.split()

    if len(args) < 2:
        await message.answer("Использование:\n/server IP:PORT")
        return

    ip_port = args[1]

    await message.answer("🔎 Проверяю сервер...")

    info = await get_server_info(ip_port)

    if not info:
        await message.answer("❌ Сервер не найден")
        return

    text = (
        f"🎮 Сервер: {info['name']}\n"
        f"📡 Статус: {info['status']}\n"
        f"👥 Онлайн: {info['players']}\n"
        f"🗺 Карта: {info['map']}\n"
        f"🌐 Адрес: {info['address']}\n"
        f"📧 Email владельца: {info['owner_email']}\n"
        f"⚙ Framework: {info['framework']}\n"
        f"📈 TPS: {info['tps']}"
    )

    await message.answer(text)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())