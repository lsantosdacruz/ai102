#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

# Actualizar config.py
with open("app/config.py", "r", encoding="utf-8") as f:
    content = f.read()

old_section = '''    # Azure Foundry Configuration
    azure_endpoint: str
    azure_api_key: str
    azure_deployment_id: str
    azure_api_version: str = "2024-08-01-preview"
    
    # Server Configuration'''

new_section = '''    # Azure OpenAI Configuration
    azure_endpoint: str
    azure_api_key: str
    azure_deployment_id: str
    azure_api_version: str = ""
    
    # System Prompt Configuration
    use_ai102_system_prompt: bool = False
    
    # Server Configuration'''

content = content.replace(old_section, new_section)

with open("app/config.py", "w", encoding="utf-8") as f:
    f.write(content)

print("[OK] config.py actualizado")

# Actualizar agent.py
with open("app/agent.py", "r", encoding="utf-8") as f:
    agent_content = f.read()

# Agregar import del sistema prompt
old_imports = '''import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Optional
import requests

from app.config import Settings

logger = logging.getLogger(__name__)'''

new_imports = '''import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Optional
import requests

from app.config import Settings

logger = logging.getLogger(__name__)

# Import system prompt if available
try:
    from system_prompt import SYSTEM_PROMPT_AI102
except ImportError:
    SYSTEM_PROMPT_AI102 = "You are a helpful assistant. Respond in the same language as the user."'''

agent_content = agent_content.replace(old_imports, new_imports)

# Actualizar __init__
old_init = '''    def __init__(self, settings: Settings):
        self.settings = settings
        # endpoint is expected like: https://<resource>.openai.azure.com/openai/v1
        self.endpoint = settings.azure_endpoint.rstrip("/")
        self.api_key = settings.azure_api_key
        # deployment name or model identifier (e.g. gpt-5-mini)
        self.model = settings.azure_deployment_id
        self.api_version = settings.azure_api_version or None'''

new_init = '''    def __init__(self, settings: Settings):
        self.settings = settings
        # endpoint is expected like: https://<resource>.openai.azure.com/openai/v1
        self.endpoint = settings.azure_endpoint.rstrip("/")
        self.api_key = settings.azure_api_key
        # deployment name or model identifier (e.g. gpt-5-mini)
        self.model = settings.azure_deployment_id
        self.api_version = settings.azure_api_version or None
        # System prompt - use AI-102 if configured
        if settings.use_ai102_system_prompt:
            self.system_prompt = SYSTEM_PROMPT_AI102
        else:
            self.system_prompt = "You are a helpful assistant. Respond in the same language as the user."'''

agent_content = agent_content.replace(old_init, new_init)

# Actualizar mensajes
old_messages = '''        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": user_message}],
            # Azure OpenAI variant expects `max_completion_tokens`
            "max_completion_tokens": max_tokens,
        }'''

new_messages = '''        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_message}
            ],
            # Azure OpenAI variant expects `max_completion_tokens`
            "max_completion_tokens": max_tokens,
        }'''

agent_content = agent_content.replace(old_messages, new_messages)

with open("app/agent.py", "w", encoding="utf-8") as f:
    f.write(agent_content)

print("[OK] agent.py actualizado")
print("\n[SUCCESS] Sistema de prompts actualizado correctamente!")
