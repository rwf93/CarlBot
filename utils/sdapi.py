import requests
import aiohttp

def txt2img(endpoint, payload): 
    return requests.post(url=f'{endpoint}/sdapi/v1/txt2img', json=payload)

def get_models(endpoint):
    return requests.get(url=f'{endpoint}/sdapi/v1/sd-models')

def get_samplers(endpoint):
    return requests.get(url=f'{endpoint}/sdapi/v1/samplers')

def get_settings(endpoint):
    return requests.get(url=f'{endpoint}/sdapi/v1/options')

def set_settings(endpoint, payload):
    return requests.post(url=f'{endpoint}/sdapi/v1/options', json=payload)

def get_styles(endpoint):
    return requests.get(url=f'{endpoint}/sdapi/v1/prompt-styles')

def get_upscalers(endpoint):
    return requests.get(url=f'{endpoint}/sdapi/v1/upscalers')

def upscale_single(endpoint, payload):
    return requests.post(url=f'{endpoint}/sdapi/v1/extra-single-image', json=payload)

async def txt2img_async(endpoint, payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f'{endpoint}/sdapi/v1/txt2img', json=payload) as resp:
            return {"json": await resp.json(), "status": resp.status}

async def upscale_single_async(endpoint, payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f'{endpoint}/sdapi/v1/extra-single-image', json=payload) as resp:
            return {"json": await resp.json(), "status": resp.status}
        