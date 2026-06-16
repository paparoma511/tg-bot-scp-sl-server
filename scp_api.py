
import aiohttp

API = "https://api.gamemonitoring.net/servers"


async def get_server_info(ip_port: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(API) as r:
            data = await r.json()

            for s in data.get("response", []):
                if ip_port in (s.get("connect") or ""):
                    return {
                        "name": s.get("name", "Unknown"),
                        "status": "🟢 Online" if s.get("status") else "🔴 Offline",
                        "players": f"{s.get('numplayers',0)}/{s.get('maxplayers',0)}",
                        "map": s.get("map", "Unknown"),
                    }

    return None