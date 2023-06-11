import aiohttp

async def async_post(endpoint: str, secondary: str, payload: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f"{endpoint}{secondary}", json=payload) as resp:
            if resp.status == 200:
                return await resp.json(), resp.status

            return None, resp.status
