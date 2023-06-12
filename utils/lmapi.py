import requests
from utils.common_async import async_post

def generate(endpoint, payload):
    return requests.post(url=f"{endpoint}/api/v1/generate", json=payload)

async def generate_async(endpoint, payload):
    return await async_post(endpoint, "/api/v1/generate", payload)
