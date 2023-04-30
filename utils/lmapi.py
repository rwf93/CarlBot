import requests
import aiohttp

def generate(endpoint, payload):
    return requests.post(url=f"{endpoint}/api/v1/generate", json=payload)