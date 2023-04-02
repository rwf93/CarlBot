import base64
import requests
import io

def txt2img(endpoint, payload): 
    return requests.post(url=f'{endpoint}/sdapi/v1/txt2img', json=payload)

def getmodels(endpoint):
    return requests.get(url=f'{endpoint}/sdapi/v1/sd-models')

def getsamplers(endpoint):
    return requests.get(url=f'{endpoint}/sdapi/v1/samplers')