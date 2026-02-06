#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick test POST to OpenAI-compatible chat completions endpoint
"""
import requests
from app.config import Settings

settings = Settings()

url = settings.azure_endpoint.rstrip('/') + '/chat/completions'
headers = {
    'api-key': settings.azure_api_key,
    'Content-Type': 'application/json'
}

payload = {
    'model': settings.azure_deployment_id,
    'messages': [
        {'role': 'user', 'content': 'Hello there — quick connectivity test.'}
    ],
    'max_tokens': 32
}

print('POST', url)
try:
    r = requests.post(url, headers=headers, json=payload, timeout=15)
    print('Status:', r.status_code)
    try:
        print('Response JSON:', r.json())
    except Exception:
        print('Response Text:', r.text)
except Exception as e:
    print('Request failed:', e)
    import traceback
    traceback.print_exc()
