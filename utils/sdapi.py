import requests

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

def get_png_info(endpoint, payload):
    return requests.post(url=f'{endpoint}/sdapi/v1/png-info', json=payload)