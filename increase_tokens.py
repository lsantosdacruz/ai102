#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Aumentar max_tokens a 4096 para manejar prompts largos
"""

with open("app/agent.py", "r", encoding="utf-8") as f:
    content = f.read()

# Cambiar default de 2048 a 4096
content = content.replace(
    'async def process_message(self, user_message: str, max_tokens: int = 2048) -> str:',
    'async def process_message(self, user_message: str, max_tokens: int = 4096) -> str:'
)

content = content.replace(
    'def _process_message_sync(self, user_message: str, max_tokens: int = 2048) -> str:',
    'def _process_message_sync(self, user_message: str, max_tokens: int = 4096) -> str:'
)

with open("app/agent.py", "w", encoding="utf-8") as f:
    f.write(content)

print("[OK] max_tokens aumentado a 4096")
