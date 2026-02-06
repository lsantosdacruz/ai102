#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test the running FastAPI /api/chat endpoint
"""
import requests
import time

url = "http://127.0.0.1:8000/api/chat"
headers = {"Content-Type": "application/json"}
json_payload = {"content": "Hello from server test"}

for attempt in range(1, 6):
    try:
        resp = requests.post(url, json=json_payload, headers=headers, timeout=10)
        print('Status:', resp.status_code)
        try:
            print('JSON:', resp.json())
        except Exception:
            print('Text:', resp.text)
        break
    except Exception as e:
        print(f'Attempt {attempt} failed: {e}')
        time.sleep(1)
else:
    print('All attempts failed')
