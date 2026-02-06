#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Debug script to test Azure Foundry agent connection
"""

import sys
from pathlib import Path

# Add the project root to path
sys.path.insert(0, str(Path(__file__).parent))

from app.config import Settings
from app.agent import AIAgent

try:
    print("=" * 60)
    print("Testing Azure Foundry Agent Connection")
    print("=" * 60)
    
    # Load settings
    settings = Settings()
    print(f"\n[OK] Settings loaded")
    print(f"  Endpoint: {settings.azure_endpoint}")
    print(f"  Agent ID: {settings.azure_deployment_id}")
    print(f"  API Version: {settings.azure_api_version}")
    print(f"  API Key (first 20 chars): {settings.azure_api_key[:20]}...")
    
    # Try to initialize agent
    print(f"\n[WAIT] Initializing AI Agent...")
    agent = AIAgent(settings)
    
    print(f"[OK] Agent initialized successfully!")
    
    print("\n" + "=" * 60)
    print("SUCCESS! Agent is ready to use.")
    print("=" * 60)
    
except Exception as e:
    print(f"\n[ERROR] {e}")
    print(f"\nFull error details:")
    import traceback
    traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("TROUBLESHOOTING STEPS:")
    print("=" * 60)
    print("1. Check your .env file:")
    print("   - AZURE_ENDPOINT should be the full project URL")
    print("   - AZURE_API_KEY should be valid and not expired")
    print("   - AZURE_DEPLOYMENT_ID should be the agent ID (asst_...)")
    print("\n2. Verify in Azure Portal:")
    print("   - Go to your AI Foundry project")
    print("   - Check that the agent exists")
    print("   - Check the API key is valid")
    print("\n3. Check the error message above for specifics")
