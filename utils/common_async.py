# because we can't have nice things
import aiohttp

async def async_post(endpoint: str, secondary: str, payload: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f"{endpoint}{secondary}", json=payload) as resp:
            if resp.status == 200:
                return await resp.json(), resp.status

            return None, resp.status

async def async_get(endpoint: str, secondary: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{endpoint}{secondary}") as resp:
            if resp.status == 200:
                return await resp.json(), resp.status

            return None, resp.status
