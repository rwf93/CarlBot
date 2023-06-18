import requests
from utils.casync import async_post

def txt2img(endpoint, payload):
    return requests.post(url=f"{endpoint}/sdapi/v1/txt2img", json=payload)

def get_models(endpoint):
    return requests.get(url=f"{endpoint}/sdapi/v1/sd-models")

def get_samplers(endpoint):
    return requests.get(url=f"{endpoint}/sdapi/v1/samplers")

def get_styles(endpoint):
    return requests.get(url=f"{endpoint}/sdapi/v1/prompt-styles")

def get_upscalers(endpoint):
    return requests.get(url=f"{endpoint}/sdapi/v1/upscalers")

def upscale_single(endpoint, payload):
    return requests.post(url=f"{endpoint}/sdapi/v1/extra-single-image", json=payload)

async def txt2img_async(endpoint: str, payload: dict):
    return await async_post(endpoint, "/sdapi/v1/txt2img", payload)

async def upscale_single_async(endpoint, payload):
    return await async_post(endpoint, "/sdapi/v1/extra-single-image", payload)

async def set_settings_async(endpoint, payload):
    return await async_post(endpoint, "/sdapi/v1/options", payload)
