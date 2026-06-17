import asyncio
import logging
import os

from aiogram import types
from aiogram.filters import Command
from scp_api import get_server_info

@dp.message(Command("server"))
async def server_handler(message: types.Message):
    args = message.text.split()

    if len(args) < 2:
        await message.answer(
            "Использование:\n/server IP:PORT"
        )
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