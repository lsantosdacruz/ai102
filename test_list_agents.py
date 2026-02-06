#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test listing agents
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
print("Testing Listing Agents")
print("=" * 60)

# Build the URL to list agents
url = f"{settings.azure_endpoint.rstrip('/')}/agents"

print(f"\n[INFO] URL: {url}")

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
            data = response.json()
            if "value" in data:
                print(f"[INFO] Found {len(data['value'])} agents:")
                for agent in data['value']:
                    print(f"  - {agent.get('id', 'N/A')}: {agent.get('name', 'N/A')}")
            else:
                print(f"[INFO] Response: {json.dumps(data, indent=2)}")
        else:
            error_msg = response.json().get("error", {}).get("message", response.text) if response.text else "No response"
            print(f"[X] API Version {api_version}: {response.status_code} - {error_msg}")
            
    except Exception as e:
        print(f"[ERROR] API Version {api_version}: {e}")
