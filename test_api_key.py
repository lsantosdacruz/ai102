#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test API key directly with REST request
"""

import requests
import json
from app.config import Settings

try:
    settings = Settings()
    
    print("=" * 60)
    print("Testing API Key with Direct REST Request")
    print("=" * 60)
    
    # Build the URL
    url = f"{settings.azure_endpoint.rstrip('/')}/agents/{settings.azure_deployment_id}"
    
    print(f"\n[INFO] URL: {url}")
    print(f"[INFO] Agent ID: {settings.azure_deployment_id}")
    print(f"[INFO] API Version: {settings.azure_api_version}")
    
    # Try to get agent
    headers = {
        "api-key": settings.azure_api_key,
        "Content-Type": "application/json"
    }
    
    params = {
        "api-version": settings.azure_api_version
    }
    
    print(f"\n[WAIT] Testing API key...")
    
    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=10
    )
    
    print(f"\n[INFO] Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print(f"[OK] SUCCESS! API Key works")
        data = response.json()
        print(f"[INFO] Agent: {data.get('name', 'N/A')}")
        print(f"[INFO] Agent ID: {data.get('id', 'N/A')}")
    else:
        print(f"[ERROR] HTTP {response.status_code}")
        print(f"[ERROR] Response: {response.text}")
    
except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()
