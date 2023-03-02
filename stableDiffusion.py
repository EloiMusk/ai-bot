import os

import requests

API_URL = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"


def query(payload, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content
