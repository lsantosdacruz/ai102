#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test different API versions
"""

import requests
import json
from app.config import Settings

settings = Settings()

api_versions = [
    "2024-08-01-preview",
    "2024-12-01-preview", 
    "2025-01-01-preview",
    "2025-04-01-preview",
]

print("=" * 60)
print("Testing Different API Versions")
print("=" * 60)

# Build the URL
url = f"{settings.azure_endpoint.rstrip('/')}/agents/{settings.azure_deployment_id}"

headers = {
    "api-key": settings.azure_api_key,
    "Content-Type": "application/json"
}

for api_version in api_versions:
    params = {"api-version": api_version}
    
    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=5
        )
        
        if response.status_code == 200:
            print(f"\n[OK] API Version {api_version} WORKS!")
        else:
            error_msg = response.json().get("error", {}).get("message", response.text)
            print(f"[X] API Version {api_version}: {response.status_code} - {error_msg}")
            
    except Exception as e:
        print(f"[ERROR] API Version {api_version}: {e}")
