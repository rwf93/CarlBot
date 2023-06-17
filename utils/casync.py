import aiohttp

async def async_post(endpoint: str, secondary: str, payload: dict):
    async with aiohttp.ClientSession() as session:
        try: # it throws an error if it flat out cannot connect, or otherwise.
            async with session.post(url=f"{endpoint}{secondary}", json=payload) as resp:
                if resp.status == 200:
                    return await resp.json(), resp.status
            return None, resp.status
        except aiohttp.ClientConnectorError as e:
            return None, e.errno

async def async_get(endpoint: str, secondary: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url=f"{endpoint}{secondary}") as resp:
                if resp.status == 200:
                    return await resp.json(), resp.status
                return None, resp.status
        except aiohttp.ClientConnectorError as e:
            return None, e.errno
