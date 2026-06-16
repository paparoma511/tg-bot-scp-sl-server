import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command

TOKEN = "8792122115:AAEGnE6tYczpsaBJz-xzds95fd-xnuSqrsQ"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- поиск сервера по IP ---
async def find_server(ip_port: str):
    url = f"https://api.gamemonitoring.net/servers"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            data = await r.json()

            for server in data.get("response", []):
                if server.get("connect") and ip_port in server["connect"]:
                    return server

    return None


# --- получение полной инфы по ID ---
async def get_server_by_id(server_id: int):
    url = f"https://api.gamemonitoring.net/servers/{server_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            return await r.json()


@dp.message(Command("server"))
async def server_info(message: Message):
    args = message.text.split()

    if len(args) < 2:
        await message.answer("Используй: /server IP:PORT")
        return

    target = args[1]

    await message.answer("Ищу сервер...")

    server = await find_server(target)

    if not server:
        await message.answer("Сервер не найден 😢")
        return

    server_id = server["id"]

    full = await get_server_by_id(server_id)
    data = full.get("response", {})

    name = data.get("name", "Unknown")
    status = "🟢 Online" if data.get("status") else "🔴 Offline"
    players = f'{data.get("numplayers", 0)}/{data.get("maxplayers", 0)}'
    map_name = data.get("map", "Unknown")

    owner = data.get("server_owner", {}).get("username", "Unknown")

    text = (
        f"🎮 <b>{name}</b>\n"
        f"📡 Status: {status}\n"
        f"👥 Players: {players}\n"
        f"🗺 Map: {map_name}\n"
        f"👤 Owner: {owner}\n"
        f"🆔 Server ID: {server_id}\n\n"
        f"⚠️ TPS / Framework / Email — недоступны через публичное API"
    )

    await message.answer(text, parse_mode="HTML")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
