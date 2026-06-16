import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import TOKEN
from scp_api import get_server_info

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

    text = (
        f"🎮 <b>{data['name']}</b>\n"
        f"📡 Статус: {data['status']}\n"
        f"👥 Онлайн: {data['players']}\n"
        f"🗺 Карта: {data['map']}\n"
        f"🆔 ID: {data['id']}\n\n"
        f"⚠️ TPS / Framework / Email — недоступны"
    )

    await message.answer(text, parse_mode="HTML")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())