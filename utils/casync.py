import aiohttp

# this is defo overkill
class ResponseError(Exception):
    def __init__(self, status: int):
        self.status = status
        super().__init__(self.status)

def error_handler(exception):
    if isinstance(exception, ResponseError):
        return None, exception.status

    if isinstance(exception, aiohttp.ClientConnectorError):
        return None, exception.errno

async def async_post(endpoint: str, secondary: str, payload: dict):
    async with aiohttp.ClientSession() as session:
        try: # it throws an error if it flat out cannot connect, or otherwise.
            async with session.post(url=f"{endpoint}{secondary}", json=payload) as resp:
                if resp.status != 200:
                    raise ResponseError(resp.status)
            return await resp.json(), resp.status
        except Exception as e:
            return error_handler(e)

async def async_get(endpoint: str, secondary: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url=f"{endpoint}{secondary}") as resp:
                if resp.status != 200:
                    raise ResponseError(resp.status)
            return await resp.json(), resp.status
        except Exception as e:
            return error_handler(e)