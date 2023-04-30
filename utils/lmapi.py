import requests
import aiohttp

def generate(endpoint, payload):
    return requests.post(url=f"{endpoint}/api/v1/generate", json=payload)

async def generate_async(endpoint, payload): 
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f"{endpoint}/api/v1/generate", json=payload) as resp:
            return {"json": await resp.json(), "status": resp.status}