import aiohttp

API_URL = "https://api.gamemonitoring.net/servers"


async def get_server_info(ip_port: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL, timeout=15) as response:
                data = await response.json()

                for server in data.get("response", []):
                    connect = server.get("connect", "")

                    if ip_port in connect:
                        return {
                            "name": server.get("name", "Неизвестно"),
                            "status": "🟢 Онлайн" if server.get("status") else "🔴 Оффлайн",
                            "players": f"{server.get('numplayers', 0)}/{server.get('maxplayers', 0)}",
                            "map": server.get("map", "Неизвестно"),
                            "address": connect,
                            "owner_email": "Недоступно",
                            "framework": "Недоступно",
                            "tps": "Недоступно"
                        }

    except Exception as e:
        print("API ERROR:", e)

    return None