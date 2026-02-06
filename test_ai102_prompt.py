#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json

url = "http://127.0.0.1:8000/api/chat"
headers = {"Content-Type": "application/json"}
json_payload = {"content": "Apresente as opções de dias de treinamento para AI-102"}

try:
    resp = requests.post(url, json=json_payload, headers=headers, timeout=10)
    print(f'Status: {resp.status_code}')
    data = resp.json()
    print(f'\nResposta:\n{data["message"]}')
except Exception as e:
    print(f'Erro: {e}')
