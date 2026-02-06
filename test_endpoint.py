#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test to discover correct API endpoint structure
"""

import requests
import json
from app.config import Settings

settings = Settings()

print("=" * 60)
print("Testing Endpoint Structure")
print("=" * 60)

print(f"\n[INFO] Endpoint from config: {settings.azure_endpoint}")
print(f"[INFO] Agent ID: {settings.azure_deployment_id}")
print(f"[INFO] API Key: {settings.azure_api_key[:10]}...{settings.azure_api_key[-5:]}")

headers = {
    "api-key": settings.azure_api_key,
    "Content-Type": "application/json"
}

# Try different endpoint variations
endpoints = [
    # With /api/projects/evaluator prefix
    (f"{settings.azure_endpoint}/agents", "With /agents suffix"),
    (f"{settings.azure_endpoint}/agents/{settings.azure_deployment_id}", "With /agents/ID"),
    # Alternative structure
    (settings.azure_endpoint, "Raw endpoint"),
    # Try root
    (settings.azure_endpoint.split("/api/")[0], "Project root"),
]

for endpoint_url, description in endpoints:
    print(f"\n[TEST] {description}")
    print(f"[INFO] URL: {endpoint_url}")
    
    try:
        # Try without version first
        response = requests.get(
            endpoint_url,
            headers=headers,
            timeout=5
        )
        print(f"[RESULT] Status: {response.status_code}")
        if response.status_code < 500:
            try:
                data = response.json()
                print(f"[RESPONSE] {json.dumps(data, indent=2)[:200]}...")
            except:
                print(f"[RESPONSE] {response.text[:200]}")
                
    except Exception as e:
        print(f"[ERROR] {e}")
