import aiohttp

# простой бесплатный API мониторинга SCP/Steam серверов
API_URL = "https://api.gamemonitoring.net/servers"


async def get_server_info(ip_port: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as r:
            data = await r.json()

            for server in data.get("response", []):
                if ip_port in (server.get("connect") or ""):
                    server_id = server.get("id")

                    return {
                        "id": server_id,
                        "name": server.get("name", "Unknown"),
                        "status": "Online" if server.get("status") else "Offline",
                        "players": f"{server.get('numplayers',0)}/{server.get('maxplayers',0)}",
                        "map": server.get("map", "Unknown")
                    }

    return None