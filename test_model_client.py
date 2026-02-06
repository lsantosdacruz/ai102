#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick test for the OpenAI-compatible AIAgent class
"""
import asyncio
from app.config import Settings
from app.agent import AIAgent

async def run_test():
    settings = Settings()
    agent = AIAgent(settings)
    resp = await agent.process_message("Hello from test_model_client. How are you?")
    print("Response:", resp)

if __name__ == '__main__':
    asyncio.run(run_test())
